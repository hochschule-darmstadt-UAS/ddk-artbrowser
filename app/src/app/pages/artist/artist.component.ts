import { Component, OnInit, OnDestroy } from '@angular/core';
import { Artist, Artwork, EntityType } from 'src/app/shared/models/models';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { ActivatedRoute } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { shuffle } from 'src/app/core/services/utils.service';

@Component({
  selector: 'app-artist',
  templateUrl: './artist.component.html',
  styleUrls: ['./artist.component.scss']
})
export class ArtistComponent implements OnInit, OnDestroy {
  /* TODO:REVIEW
    Similiarities in every page-Component:
    - variables: ngUnsubscribe, collapse, sliderItems, dataService, route
    - ngOnDestroy, calculateCollapseState, ngOnInit

    1. Use Inheritance (Root-Page-Component) or Composition
    2. Inject entity instead of artist
  */

  /** The entity this page is about */
  artist: Artist = null;
  /** Related artworks */
  sliderItems: Artwork[] = [];
  /** use this to end subscription to url parameter in ngOnDestroy */
  private ngUnsubscribe = new Subject();

  /** Toggle bool for displaying either timeline or artworks carousel component */
  showTimelineNotArtworks = true;

  constructor(private dataService: DataService, private route: ActivatedRoute) {}

  /** hook that is executed at component initialization */
  ngOnInit() {
    /** Extract the id of entity from URL params. */
    this.route.paramMap.pipe(takeUntil(this.ngUnsubscribe)).subscribe(async params => {
      const artistId = params.get('artistId');
      /** Use data service to fetch entity from database */
      this.artist = await this.dataService.findById<Artist>(artistId, EntityType.ARTIST);

      /** load slider items */
      this.dataService.findArtworksByType(EntityType.ARTIST, [this.artist.id]).then(artworks => (this.sliderItems = shuffle(artworks)));
    });
  }

  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  toggleComponent() {
    this.showTimelineNotArtworks = !this.showTimelineNotArtworks;
  }
}
