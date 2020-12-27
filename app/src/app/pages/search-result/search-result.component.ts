import { Component, OnInit, OnDestroy } from '@angular/core';
import { Artwork, EntityType, Entity, EntityIcon, ArtSearch } from 'src/app/shared/models/models';
import { ActivatedRoute } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { Angulartics2 } from 'angulartics2';
import { usePlural } from 'src/app/shared/models/entity.interface';

/**
 * @description Interface for the search results.
 * @export
 */
export interface SearchResult {
  items: Entity[];
  key: EntityType;
  icon: EntityIcon;
}

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit, OnDestroy {
  /** Related artworks */
  sliderItems: Artwork[] = [];

  /**
   * variable of the search results
   */
  searchResults: SearchResult[] = [];

  /**
   * specific search terms
   */
  searchTerms: string[] = [];

  /** use this to end subscription to url parameter in ngOnDestroy */
  private ngUnsubscribe = new Subject();

  constructor(private dataService: DataService, private route: ActivatedRoute, private angulartics2: Angulartics2) {}

  /** hook that is executed at component initialization */
  ngOnInit() {
    /** Extract the search params from url query params. */
    this.route.queryParams.pipe(takeUntil(this.ngUnsubscribe)).subscribe(async params => {
      /** resets search results  */
      this.searchResults = [];
      this.searchTerms = params.term ? (Array.isArray(params.term) ? params.term : [params.term]) : [];
      if (params.artist) {
        this.searchResults.push(await this.getSearchResults(params.artist, EntityType.ARTIST, EntityIcon.ARTIST));
      }
      if (params.genre) {
        this.searchResults.push(await this.getSearchResults(params.genre, EntityType.GENRE, EntityIcon.GENRE));
      }
      if (params.type) {
        this.searchResults.push(await this.getSearchResults(params.type, EntityType.TYPE, EntityIcon.TYPE));
      }
      if (params.location) {
        this.searchResults.push(await this.getSearchResults(params.location, EntityType.LOCATION, EntityIcon.LOCATION));
      }
      if (params.material) {
        this.searchResults.push(await this.getSearchResults(params.material, EntityType.MATERIAL, EntityIcon.MATERIAL));
      }
      if (params.iconography) {
        this.searchResults.push(await this.getSearchResults(params.iconography, EntityType.ICONOGRAPHY, EntityIcon.ICONOGRAPHY));
      }
      this.sliderItems = await this.getSliderItems(this.searchResults, this.searchTerms);

      this.angulartics2.eventTrack.next({
        action: 'trackSiteSearch',
        properties: {
          category: 'Search page',
          keyword: this.searchTerms.toString(),
          searchCount: this.sliderItems.length
        }
      });
    });
  }

  /**
   * Get multiple entities by ids. Return search result object.
   * @param ids id arrays
   * @param type filter by type
   * @param icon icon for SearchResult.
   */
  private async getSearchResults<T>(ids: [], type: EntityType, icon: EntityIcon): Promise<SearchResult> {
    const items = (await this.dataService.findMultipleById<T>([].concat(ids), type)) as any[];
    return { items, icon, key: type };
  }

  /**
   * Search artworks by ids and terms
   * Return artwork array
   * @param results search result array
   * @param terms terms array
   */
  private async getSliderItems(results: SearchResult[], terms: string[]): Promise<Artwork[]> {
    const search: ArtSearch = {};
    results.forEach(typeArray => (search[usePlural(typeArray.key)] = typeArray.items.map((e: Entity) => e.id)));
    return await this.dataService.searchArtworks(search, terms);
  }

  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }
}
