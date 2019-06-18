import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { DataService } from 'src/app/core/services/data.service';
import { Router } from '@angular/router';
import { debounceTime, switchMap } from 'rxjs/operators';
import { TagItem } from '../../models/models';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit {
  /**
   * @description input for search component
   */
  searchInput: string;

  /**
   * @description simple check to prep tag for removal
   */
  rmTag: boolean = false;

  /** whether search is header or home page */
  @Input()
  isHeaderSearch = false;

  /**
   * @description Array of all chips.
   */
  searchItems: TagItem[] = [];

  constructor(private dataService: DataService, private router: Router) {}

  ngOnInit() {}

  /**
   * @description basic type-ahead function for search bar.
   * This function get objects from data service,
   * sort objects and filter by criteria,
   * slice to return limited number of objects
   */
  formatter = (x: { name: string }) => x.name;

  public search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      switchMap(async (term) => {
        if (term === '') {
          return [];
        }
        let entities = await this.dataService.findEntitiesByLabelText(term.toLowerCase());
        entities = entities
          .filter((v) => v.label.toLowerCase().indexOf(term.toLowerCase()) > -1)
          .sort(
            (a, b): any => {
              let rankA = a.relativeRank;
              let rankB = b.relativeRank;
              const typeA = a.type;
              const typeB = b.type;
              const aPos = a.label.toLowerCase().indexOf(term.toLowerCase());
              const bPos = b.label.toLowerCase().indexOf(term.toLowerCase());

              if (typeB < typeA) {
                return 1;
              } else if (typeA < typeB) {
                return -1;
              }
              // factor 2 for initial position
              if (aPos === 0) {
                rankA *= 2;
              }
              if (bPos === 0) {
                rankB *= 2;
              }
              // factor 0.5 for non-whitespace in front
              if (
                aPos > 0 &&
                a.label
                  .toLowerCase()
                  .charAt(aPos - 1)
                  .match(/\S/)
              ) {
                rankA *= 0.5;
              }
              if (
                bPos > 0 &&
                b.label
                  .toLowerCase()
                  .charAt(bPos - 1)
                  .match(/\S/)
              ) {
                rankA *= 0.5;
              }
              return rankB > rankA ? 1 : rankB < rankA ? -1 : 0;
            }
          )
          //TODO: i think instead of using .filter we should write an own function for it.
          .filter(
            (w, i, arr) =>
              (w.type === 'artist' && // if type is artwork or artist, take 3
                w.type !== (arr[i - 3] ? arr[i - 3].type : '')) ||
              (w.type !== 'artwork' &&
              w.type !== 'artist' && // if type is other type, take 2
                w.type !== (arr[i - 2] ? arr[i - 2].type : '')) ||
              (w.type === 'artwork' && w.type !== (arr[i - 3] ? arr[i - 3].type : ''))
          ) // To Do: get more suggestion if list does not have enough elements
          .slice(0, 10)
          .sort(
            (a, b): any => {
              let typeA = a.type;
              let typeB = b.type;
              if ((typeA === 'artist' || typeA === 'artwork') && (typeB === 'artwork' || typeB === 'artist')) {
                // switch place of artist and artwork
                if (typeB < typeA) {
                  return -1;
                } else if (typeA < typeB) {
                  return 1;
                }
              }
            }
          );
        return this.searchInput ? entities : [];
      })
    );

  /**
   * @description function called when selecting an item in type-ahead suggestions
   * based on type of item
   */
  public async itemSelected($event) {
    this.searchInput = '';
    let url = `/${$event.item.type}/${$event.item.id}`;
    if ($event.item.type === 'object') {
      url = `/motif/${$event.item.id}`;
    }

    if ($event.item.type !== 'artwork') {
      this.searchItems.push({
        label: $event.item.label,
        type: $event.item.type,
        id: $event.item.id,
      });
      $event.preventDefault();
    }
    this.router.navigate([url]);
  }

  /** build query params for search result url */
  buildQueryParams() {
    let params = {
      term: [],
      artist: [],
      motif: [],
      movement: [],
      genre: [],
      material: [],
      location: [],
    };
    for (const item of this.searchItems) {
      if (!item.type) {
        params.term.push(item.label);
      } else {
        switch (item.type) {
          case 'artist': {
            params.artist.push(item.id);
            break;
          }
          case 'movement': {
            params.movement.push(item.id);
            break;
          }
          case 'genre': {
            params.genre.push(item.id);
            break;
          }
          case 'material': {
            params.material.push(item.id);
            break;
          }
          case 'object': {
            params.motif.push(item.id);
            break;
          }
          case 'location': {
            params.location.push(item.id);
            break;
          }
        }
      }
    }
    return params;
  }

  /**
   * @description search for string when no item is selected
   */
  public navigateToSearchText(term) {
    if (term !== '' && !(term instanceof Object)) {
      this.searchItems.push({
        label: term,
        type: null,
        id: null,
      });
    }
    this.searchInput = '';
    this.router.navigate(['/search'], { queryParams: this.buildQueryParams() });
  }

  /**
   * @description search items when there are chips and no input
   */
  public searchText() {
    this.navigateToSearchText(this.searchInput);
  }

  /**
   * @description remove chip from search bar
   */
  public removeTag(item: TagItem) {
    this.searchItems = this.searchItems.filter((i) => i !== item);
  }

  /**
   * @description get chips ready to be removed.
   * used to prevent backspace to accidentally delete all chips
   */
  public readyToRemove() {
    if (this.searchInput === '' && this.searchItems.length > 0) {
      this.rmTag = true;
    }
  }
  /**
   * @description remove newest chip
   */
  public removeNewestTag() {
    if (this.searchInput === '' && this.rmTag === true) {
      this.searchItems.splice(this.searchItems.length - 1, 1);
    }
    this.rmTag = false;
  }

  /**
   * @description remove all chips
   */
  public clearAllTags() {
    this.searchItems = [];
  }
}
