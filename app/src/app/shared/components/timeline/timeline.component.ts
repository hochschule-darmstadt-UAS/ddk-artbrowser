import { Component, Input, HostListener, OnChanges } from '@angular/core';
import { Artist, Artwork, Entity, EntityType } from 'src/app/shared/models/models';
import { CustomStepDefinition, Options } from '@angular-slider/ngx-slider';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import * as _ from 'lodash';
import { getYearFromString } from 'src/app/core/services/ddk.service';

interface TimelineItem extends Entity {
  description: string;
  date: number; // represents the value the item is located in the timeline
}

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
  animations: [
    trigger('slideNext', [
      state('out', style({ transform: 'translateX(7%)', opacity: 0 })),
      state('in', style({ transform: 'translateX(0)', opacity: 1 })),
      transition('in => out', [animate(0)]),
      transition('out => in', [animate(300)])
    ]),
    trigger('slidePrev', [
      state('out', style({ transform: 'translateX(-7%)', opacity: 0 })),
      state('in', style({ transform: 'translateX(0)', opacity: 1 })),
      transition('in => out', [animate(0)]),
      transition('out => in', [animate(300)])
    ])
  ]
})
export class TimelineComponent implements OnChanges {
  /** Artworks that should be displayed in this slider */
  @Input() artworks: Artwork[] = [];
  /** Decide whether artists should be displayed */
  @Input() displayArtists = false;

  /** TimelineItems that should be displayed in this slider */
  items: TimelineItem[] = [];
  private periodSpan = 1;

  private maxSliderSteps = 1000;
  /** Specifies the amount of items displayed once at a time */
  private itemCountPerPeriod = 4;
  /** Specifies the average amount of labels on the slider */
  private averagePeriodCount: number;

  /** Index of the starting and ending items */
  slideStart: number;
  slideEnd: number;

  /** Controls carousel movement by the slider
   *  In case the carousel moves the timeline, the timeline
   *  event should not move the carousel for its part
   */
  private sliderAllowEvent = true;

  /** Controls carousel animations */
  slideOutRight = false;
  slideOutLeft = false;

  /** The reference item describes the index of the item referring
   *  to the displayed value in the slider.
   *  It is either the first or second item (Values 0 or 1)
   *  It is only 0 if only one item is displayed per period
   */
  private referenceItem: number;

  /** The current value of the slider */
  value: number;
  /** Used to determine which animation direction to trigger when slider was clicked */
  previousValue: number;
  /** Settings for slider component */
  options: Options = {
    showTicksValues: false,
    showTicks: true,
    showSelectionBar: false,
    stepsArray: [],
    getPointerColor() {
      return '#00bc8c';
    },
    getTickColor() {
      return '#FFFFFF00';
    },
    customValueToPosition(val, minVal, maxVal) {
      const range = maxVal - minVal;
      return (val - minVal) / range;
    },
    customPositionToValue(percent, minVal, maxVal) {
      return percent * (maxVal - minVal) + minVal;
    }
  };

  /** Determine values based on screen width (responsivity) */
  @HostListener('window:resize', ['$event'])
  onResize() {
    const screenWidth = window.innerWidth;
    /** Set itemCountPerPeriod to value between 1 and 4, depending on screen width */
    this.itemCountPerPeriod = Math.min(4, Math.max(1, Math.floor(screenWidth / 300)));
    /** decide whether reference item should be 0 or 1 */
    this.referenceItem = +(this.itemCountPerPeriod > 1 && this.items.length > 1); // Convert bool to int, cause i can, LOL
    /** Determine the amount of marked steps in the slider, depending on screen width */
    this.averagePeriodCount = Math.min(7, Math.floor(screenWidth / 125));
    this.refreshComponent();
  }

  constructor(private dataService: DataService) {
    this.onResize();
  }

  ngOnChanges() {
    if (typeof this.artworks !== 'undefined' && this.artworks.length > 0) {

      /** Clear items */
      this.items = [];
      this.buildTimelineItemsFromArtworks();
      if (this.displayArtists) {
        /** Insert artists into items */
        this.getArtistTimelineItems().then(artists => {
          this.items = this.items.concat(artists);
          this.sortItems();
          this.refreshComponent();
        });
      }
      this.sortItems();
      this.items = this.items.filter(item => item.date);
      if (!this.items.length) {
        return;
      }
      this.onResize();

      const beginOfTimeline = +this.items[0].date - (this.items[0].date % this.periodSpan);
      const endOfTimeline = +this.items[this.items.length - 1].date -
        (this.items[this.items.length - 1].date % this.periodSpan) + this.periodSpan;
      // Set the slider of the timeline to the middle!
      this.value = +(beginOfTimeline + endOfTimeline) / 2;
      this.previousValue = this.value;
      this.refreshComponent();
    }
  }

  /** This method should be called whenever the timeline should adapt to new circumstances like new width or items */
  private refreshComponent() {
    if (typeof this.items !== 'undefined' && this.items.length > 0) {
      this.calculatePeriod();
      this.calcSlideStart();
      this.updateSliderItems();
    }
  }

  /**
   *  Calculates and sets the slider legend based on averagePeriodCount,
   *  this influences not the amount of steps of the slider
   */
  private calculatePeriod() {
    let sliderSteps: CustomStepDefinition[] = [];

    const firstDate = +this.items[0].date;
    const lastDate = +this.items[this.items.length - 1].date;

    const dateSpan = lastDate - firstDate;

    /** The period span must be either a multiple of reasonablePeriodDistance or minimumPeriodDistance */
    const reasonablePeriodDistance = 5;
    const minimumPeriodDistance = 1;
    /** Example:  30/7 = 4,28 ; 4,28 / 5 = 0,85 ; Math.max( Math.round(0.85)*5, 1) = 5 */
    this.periodSpan = Math.max(Math.round(dateSpan / this.averagePeriodCount /
      reasonablePeriodDistance) * reasonablePeriodDistance, minimumPeriodDistance);

    /** get the biggest multiple of periodSpan that is less than firstDate / same for lastDate */
    const firstPeriod = firstDate - (firstDate % this.periodSpan);
    const lastPeriod = lastDate - (lastDate % this.periodSpan) + this.periodSpan;

    /** Fill the slider steps with period legends respectively steps */
    const timeDifference = lastPeriod - firstPeriod;
    if (timeDifference <= this.maxSliderSteps) {
      for (let i = firstPeriod; i <= lastPeriod; i++) {
        if (i % this.periodSpan === 0) {
          sliderSteps.push({ value: i, legend: '' + i });
        } else {
          sliderSteps.push({ value: i });
        }
      }
    } else {
      /** if timeDifference bigger than maxSliderSteps, use the date values of the items */
      sliderSteps = this.items.map((item, index) => {
        const step = { value: +item.date, legend: '' };
        if (index % Math.floor(this.items.length / this.averagePeriodCount) === 0 || this.items.length < this.averagePeriodCount) {
          step.legend = item.date.toString();
        }
        return step;
      });
      sliderSteps = _.uniqBy(sliderSteps, 'value');
      sliderSteps.unshift({
        value: firstPeriod,
        legend: firstPeriod + ''
      });
      sliderSteps.push({
        value: lastPeriod,
        legend: lastPeriod + ''
      });
    }

    /** Set slider options */
    const newOptions: Options = Object.assign({}, this.options);
    newOptions.stepsArray = sliderSteps;
    newOptions.minLimit = timeDifference <= this.maxSliderSteps ? firstDate - firstPeriod : 1;
    newOptions.maxLimit = timeDifference <= this.maxSliderSteps ? lastDate - firstPeriod : sliderSteps.length - 2;
    this.options = newOptions;
  }

  /**
   * Calculate the starting index of the displayed items relative to items
   */
  private calcSlideStart() {
    /** How many of the displayed items should have a date less/equal to the slider value */
    const itemCountSmallerReference = 2;
    /** Amount of items where date is the exact slider value */
    const countReference = this.items.filter(item => +item.date === this.value).length;

    /** ReferenceIndex is the index of the first item with date equal to slider value or bigger */
    let referenceIndex: number;
    if (countReference > itemCountSmallerReference) {
      referenceIndex = this.items.findIndex(item => +item.date === this.value);
    } else {
      const firstBiggerRef = this.items.findIndex(item => +item.date > this.value);
      referenceIndex = firstBiggerRef > 0 ? firstBiggerRef - 1 : this.items.length - (this.itemCountPerPeriod - 1);
    }

    /** Determine start index */
    if (0 >= referenceIndex - 1 && referenceIndex <= this.items.length - 3) {
      // first slide
      this.slideStart = 0;
    } else if (referenceIndex + (this.itemCountPerPeriod - this.referenceItem) > this.items.length) {
      // last slide
      this.slideStart = this.items.length - this.itemCountPerPeriod;
    } else {
      // between
      this.slideStart = referenceIndex - this.referenceItem;
    }
  }

  /** This refreshes the ending index of the displayed items according to the start value */
  private updateSliderItems() {
    this.slideEnd = this.slideStart + this.itemCountPerPeriod;
  }

  /** Handler for valueChange event from slider.
   * Sets slideStart, slideEnd and value according to the new value and handles animation
   */
  onSliderMoved() {
    /** Check if event should happen */
    if (!this.sliderAllowEvent) {
      this.sliderAllowEvent = true;
      return;
    }
    this.calcSlideStart();
    this.updateSliderItems();

    /** Set the value to the date of the chosen referenceItem */
    this.value = +this.items[this.slideStart + this.referenceItem].date;
    /** Set animation */
    if (this.value > this.previousValue) {
      this.slideOutRight = true;
    } else if (this.value < this.previousValue) {
      this.slideOutLeft = true;
    }
    this.previousValue = this.value;
  }

  /** Handler for click event from left control button. Updates startSlide, value and animation. */
  prevClicked() {
    if (this.slideStart <= 0) {
      // Return if first slide
      return;
    }
    this.slideOutLeft = true;
    this.slideStart = Math.max(this.slideStart - this.itemCountPerPeriod, 0);
    this.value = +this.items[this.slideStart + this.referenceItem].date;
    // decide if sliderMoved-Event should be suppressed
    this.sliderAllowEvent = false;
    this.updateSliderItems();
  }

  /** Handler for click event from right control button. Updates startSlide, value and animation. */
  nextClicked() {
    if (this.slideEnd >= this.items.length) {
      // Return if last slide
      return;
    }
    this.slideOutRight = true;
    this.slideStart = Math.min(this.slideStart + 2 * this.itemCountPerPeriod, this.items.length) - this.itemCountPerPeriod;
    this.value = +this.items[this.slideStart + this.referenceItem].date;
    // decide if sliderMoved-Event should be suppressed
    this.sliderAllowEvent = false;

    this.updateSliderItems();
  }

  /** resets slide animation. Gets called after each animation */
  resetSlideAnimation() {
    this.slideOutRight = false;
    this.slideOutLeft = false;
  }

  /** Transform artworks into TimelineItems to display them aside with artists */
  private buildTimelineItemsFromArtworks() {
    this.artworks.forEach(artwork => {
      this.items.push({
        id: artwork.id,
        label: artwork.label,
        image: this.artworks[0].image,
        imageSmall: this.artworks[0].imageMedium,
        imageMedium: this.artworks[0].imageSmall,
        entityType: artwork.entityType,
        count: artwork.count,
        rank: artwork.rank,
        description: artwork.inception,
        date: getYearFromString(artwork.inception + '')
      } as unknown as TimelineItem);
    });
    this.items = this.items.filter(item => !isNaN(item.date));
  }

  /** This adds artists to the timeline according to the displayed artworks. The artists get placed at their birth date */
  private async getArtistTimelineItems() {
    const artists: TimelineItem[] = [];
    const artistIds: Set<string> = new Set();
    /** Get the artist ids from the top 10% ranked artworks to display them aside with artworks */
    this.artworks
      .sort((a, b) => (a.rank > b.rank ? 1 : -1))
      .slice(0, Math.max(10, Math.floor(this.artworks.length / 10))) // get top 10%
      .forEach(artwork => {
        if (artwork.artists) {
          artwork.artists.forEach(artistId => artistIds.add(artistId + ''));
        }
      });
    /** Transform artists into Timeline items and set description */
    await this.dataService.findMultipleById(Array.from(artistIds) as any, EntityType.ARTIST).then((artworkArtists: Artist[]) => {
      artworkArtists.forEach(async artist => {
        // TODO: Refactor
        const dateOfBirth = +artist.dateOfBirth || +artist.evidenceFirst;
        const dateOfDeath = +artist.dateOfDeath || +artist.evidenceLast;
        if (artist.imageSmall && (dateOfBirth || dateOfDeath)) {
          // decide whether to use date of birth or date of death for sorting (default: date of birth)
          // and set description accordingly
          let artistDescription;
          if (dateOfBirth && dateOfDeath) {
            artistDescription = `${dateOfBirth} - ${dateOfDeath}`;
          } else if (dateOfBirth) {
            artistDescription = `*${dateOfBirth}`;
          } else {
            artistDescription = '†' + dateOfDeath;
          }
          let artistSortDate;
          if (dateOfBirth && dateOfDeath) {
            artistSortDate = Math.floor(dateOfBirth + (dateOfDeath - dateOfBirth) * 0.33);
          } else if (dateOfBirth) {
            artistSortDate = dateOfBirth;
          } else {
            artistSortDate = dateOfDeath;
          }

          artists.push({
            id: artist.id,
            label: artist.label,
            image: artist.image,
            imageSmall: artist.imageSmall,
            imageMedium: artist.imageMedium,
            entityType: artist.entityType,
            count: artist.count,
            rank: artist.rank,
            date: artistSortDate,
            description: artistDescription
          } as TimelineItem);
        }
      });
    });
    return artists;
  }

  /** This sorts the component items by date */
  private sortItems() {
    // rebuild slides if slider items input changed.
    this.items.sort((a, b) => (a.date > b.date ? 1 : -1));
  }

  /** Removes items from the component which cannot be displayed */
  onLoadingError(item: TimelineItem) {
    this.items.splice(
      this.items.findIndex(i => i.id === item.id),
      1
    );
    this.refreshComponent();
  }
}
