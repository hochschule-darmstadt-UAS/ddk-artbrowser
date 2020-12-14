import { Component, OnInit, ViewChildren, QueryList } from '@angular/core';
import { NgbCarouselConfig, NgbCarousel } from '@ng-bootstrap/ng-bootstrap';
import { Entity, Artist, Artwork, Material, Location, Genre, Type, EntityIcon, EntityType } from 'src/app/shared/models/models';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { shuffle } from 'src/app/core/services/utils.service';

/**
 * @description Interface for the category sliders.
 * @export
 */
export interface SliderCategory {
  items: Entity[];
  type: EntityType;
  icon: EntityIcon;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  /**
   * @description all 7 carousels in the page.
   */
  @ViewChildren(NgbCarousel) carousel: QueryList<NgbCarousel>;

  /**
   * @description random url image for the page background
   */
  backgroundImageUrl: string;

  /**
   * @description variable of object to be fetch in html
   */
  Object = Object;

  /**
   * variable of the categories.
   */
  categories: SliderCategory[] = [];

  constructor(public dataService: DataService, ngbConfig: NgbCarouselConfig) {
    /** set configuration of ngbCarousel */
    ngbConfig.interval = 10000;
    ngbConfig.keyboard = false;
    ngbConfig.pauseOnHover = true;
  }

  ngOnInit() {
    this.setBackground();
    this.getSlides().then(slides => {
      // Fetch items for each category using the service;
      this.categories = slides;

      // need to have a bit delay of time (last categories that is fetched is not refreshing carousel cycle)
      setTimeout(() => this.refreshCarousel(), 500);

      // assign backgroundImageUrl with a random image from one of the artworks.
      this.setBackground();
    });
  }

  /**
   * removes entity from category suggestions if image of item cannot be loaded
   * @param category category the item should be removed from
   * @param item item that should be removed
   */
  onLoadingError(category: SliderCategory, item: Entity) {
    category.items = category.items.filter(i => item.id !== i.id);
  }

  /**
   * @description Fetch items for each category using the service. Return an array of slider category items.
   */
  private getSlides = async (): Promise<SliderCategory[]> => {
    const cats = [];
    cats.push(await this.getSliderCategory<Artwork>(EntityType.ARTWORK));
    cats.push(await this.getSliderCategory<Artist>(EntityType.ARTIST));
    cats.push(await this.getSliderCategory<Location>(EntityType.LOCATION));
    cats.push(await this.getSliderCategory<Material>(EntityType.MATERIAL));
    cats.push(await this.getSliderCategory<Genre>(EntityType.GENRE));
    cats.push(await this.getSliderCategory<Type>(EntityType.TYPE));
    return cats;
  }

  /**
   * @description Get categories by entity type. Return SliderCategory object.
   */
  private async getSliderCategory<T>(category: EntityType): Promise<SliderCategory> {
    const items = shuffle(await this.dataService.getCategoryItems<T>(category));
    return { items, type: category, icon: EntityIcon[category.toUpperCase()] };
  }

  private setBackground() {
    // assign backgroundImageUrl with a random image from one of the artworks.
    const artworks = this.categories && this.categories.length ? this.categories[0].items : [];
    if (artworks.length > 0) {
      this.backgroundImageUrl = artworks[Math.floor(Math.random() * artworks.length)].imageMedium;
    }
  }

  /**
   * @description make auto next carousel works after fetching categories.
   */
  private refreshCarousel(): void {
    this.carousel.forEach(item => item.cycle());
  }
}
