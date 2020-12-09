import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { Artwork, EntityIcon, EntityType } from 'src/app/shared/models/models';
import { takeUntil } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { Subject } from 'rxjs';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { shuffle } from 'src/app/core/services/utils.service';
import { usePluralAttributes } from 'src/app/shared/models/entity.interface';

/** interface for the tabs */
interface ArtworkTab {
  type: EntityType;
  items: Artwork[];
  icon: EntityIcon;
  active: boolean;
}

@Component({
  selector: 'app-artwork',
  templateUrl: './artwork.component.html',
  styleUrls: ['./artwork.component.scss']
})
export class ArtworkComponent implements OnInit, OnDestroy {
  /* TODO:REVIEW
    Similarities in every page-Component:
    - variables: ngUnsubscribe, collapse (here: detailsCollapsed), dataService, route
    - ngOnDestroy, calculateCollapseState, ngOnInit

    1. Use Inheritance (Root-Page-Component) or Composition
    2. Inject entity instead of artwork
  */

  /**
   * @description the entity this page is about.
   */
  artwork: Artwork = null;

  /**
   * whether artwork image should be hidden
   */
  imageHidden = false;

  /**
   * @description to toggle common tags container.
   * initial as false (open).
   */
  commonTagsCollapsed = false;

  /**
   * @description whether artwork image viewer is active or not
   */
  modalIsVisible = false;

  /**
   * @description to save the artwork item that is being hovered.
   */
  hoveredArtwork: Artwork = null;

  /**
   * @description for the tabs in slider/carousel.
   */
  artworkTabs: ArtworkTab[] = [];

  /**
   * @description image array for thumbnails
   */
  thumbnails: Array<object> = [];

  /** Index of current Image in artwork.resources array */
  imageIndex = 0;

  /**
   * @description use this to end subscription to url parameter in ngOnDestroy
   */
  private ngUnsubscribe = new Subject();

  constructor(private dataService: DataService, private route: ActivatedRoute) {
  }

  /**
   * @description hook that is executed at component initialization
   */
  ngOnInit() {
    // define tabs if not set
    if (!this.artworkTabs || !this.artworkTabs.length) {
      this.addTab(EntityType.ALL, true);
      this.addTab(EntityType.ICONOGRAPHY);
      this.addTab(EntityType.TYPE);
      this.addTab(EntityType.ARTIST);
      this.addTab(EntityType.LOCATION);
      this.addTab(EntityType.GENRE);
      this.addTab(EntityType.MATERIAL);
    }

    /** Extract the id of entity from URL params. */
    this.route.paramMap.pipe(takeUntil(this.ngUnsubscribe)).subscribe(async (params) => {
      /* reset properties */
      this.artwork = this.hoveredArtwork = this.hoveredArtwork = null;
      this.imageHidden = this.modalIsVisible = this.commonTagsCollapsed = false;
      // clears items of all artwork tabs
      this.artworkTabs = this.artworkTabs
        .map((tab: ArtworkTab) => {
          if (tab.type === ('main_motif' as EntityType)) {
            return null;
          }
          return { ...tab, items: [] };
        })
        .filter((tab) => tab !== null);

      /** Use data service to fetch entity from database */
      const artworkId = params.get('artworkId');
      this.artwork = await this.dataService.findById<Artwork>(artworkId, EntityType.ARTWORK);
      this.artwork.genres = this.artwork.genres.filter((value) => value !== 'IMAGE'); // This is weird but it works :)
      if (this.artwork) {
        await this.resolveIds('main_subjects');
        /* load tabs content */
        this.loadTabs();
      }

      // --- TODO: REMOVE THIS SAMPLE ---
      this.artwork.resources.push({
        image: 'http://previous.bildindex.de/bilder/d/fm1563345',
        imageSmall: 'http://previous.bildindex.de/bilder/t/fm1563345'
      });
      this.artwork.resources.push({
        image: 'http://previous.bildindex.de/bilder/d/fm1563251',
        imageSmall: 'http://previous.bildindex.de/bilder/t/fm1563251'
      });
      this.artwork.resources.push({
        image: 'http://previous.bildindex.de/bilder/d/fm1563245',
        imageSmall: 'http://previous.bildindex.de/bilder/t/fm1563245'
      });
      this.artwork.resources.push({
        image: 'http://previous.bildindex.de/bilder/d/fm1522245',
        imageSmall: 'http://previous.bildindex.de/bilder/t/fm1522245'
      });
      // ------------------------------

      this.artwork.resources.forEach(res => this.thumbnails.push({ image: res.image, thumbImage: res.imageSmall }));
      console.log(this.thumbnails);
    });
  }

  /**
   * resolves Ids to actual entities
   * @param key attribute on this.artwork
   */
  async resolveIds(key: string) {
    this.artwork[key] = await this.dataService.findMultipleById(this.artwork[key] as string[]);
  }

  /**
   * hide artwork image
   */
  hideImage() {
    this.imageHidden = true;
  }

  /**
   * @description show popup image zoom.
   */
  showModal() {
    this.modalIsVisible = true;
  }

  /**
   * @description close popup image zoom.
   */
  closeModal() {
    this.modalIsVisible = false;
  }

  /**
   * @description close popup image zoom with escape key
   */
  @HostListener('window:keydown.esc') escEvent() {
    this.closeModal();
  }

  /**
   * @description Hook that is called when a directive, pipe, or service is destroyed.
   */
  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  /**
   * resolves ids in artwork attributes with actual entities,
   * loads slider items and initializes slider tabs
   */
  private loadTabs() {
    /** get all tab */
    const allTab = this.artworkTabs.filter((tab: ArtworkTab) => tab.type === EntityType.ALL).pop();

    /** load artist related data */
    Promise.all(
      /** load related data for each tab  */
      this.artworkTabs.map(async (tab: ArtworkTab) => {
        if (tab.type === EntityType.ALL || tab.type === ('main_motif' as EntityType)) {
          return;
        }

        const types = usePluralAttributes(tab.type);

        // load entities
        this.dataService.findMultipleById([].concat(this.artwork[types] as any), tab.type).then((artists) => {
          this.artwork[types] = artists;
        });
        // load related artworks by type
        return await this.dataService.findArtworksByType(tab.type, [].concat(this.artwork[types] as any)).then((artworks) => {
          // filters and shuffles main artwork out of tab items,
          tab.items = shuffle(artworks).filter((artwork) => artwork.id !== this.artwork.id);
          // put items into 'all' tab
          allTab.items.push(...tab.items.slice(0, 10));
        });
      })
    ).then(
      () =>
        // filter duplicates and shuffles it
        (allTab.items = shuffle(Array.from(new Set(allTab.items))))
    );
  }

  /**
   * Add tab to artwork tab array
   * @param type Tab title
   * @param active Is active tab
   */
  private addTab(type: EntityType, active: boolean = false) {
    this.artworkTabs.push({
      active,
      icon: EntityIcon[type.toUpperCase()],
      type,
      items: []
    });
  }

  thumbnailClicked($event) {
    if (this.artwork.resources.length > $event) {
      this.imageIndex = $event;
    }
  }
}
