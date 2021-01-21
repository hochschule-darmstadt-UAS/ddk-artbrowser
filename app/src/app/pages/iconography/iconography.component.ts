import { Component, ElementRef, Inject, LOCALE_ID, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { Subject } from 'rxjs';
import { IconclassService } from '../../core/services/iconclass/iconclass.service';
import { Iconography } from '../../shared/models/iconography.interface';
import { Entity, EntityType } from '../../shared/models/entity.interface';
import { Artwork } from '../../shared/models/artwork.interface';
import { shuffle } from '../../core/services/utils.service';
import { DataService } from '../../core/services/elasticsearch/data.service';

@Component({
  selector: 'app-iconography',
  templateUrl: './iconography.component.html',
  styleUrls: ['./iconography.component.scss']
})
export class IconographyComponent implements OnInit {
  notation: string;
  notationExists = true;
  iconclassData: Iconography;
  hierarchy: Entity[];
  hasIconographyChildren = false;

  children: Iconography[] = [];
  parents: Iconography[] = [];

  /** Related artworks */
  sliderItemsCurrentIconography: Artwork[] = [];

  sliderItemsChildrenIconography: Artwork[] = [];

  /**
   * @description use this to end subscription to url parameter in ngOnDestroy
   */
  private ngUnsubscribe = new Subject();
  private readonly ISO_639_1_LOCALE: string;

  showCurrentIconographyArtworks = true;

  constructor(
    private dataService: DataService,
    private iconclassService: IconclassService,
    private route: ActivatedRoute,
    @Inject(LOCALE_ID) localeId: string
  ) {
    this.ISO_639_1_LOCALE = localeId.substr(0, 2);
  }

  ngOnInit() {
    this.route.paramMap.pipe(takeUntil(this.ngUnsubscribe)).subscribe(async params => {
      this.notation = params.get('notation');
      this.iconclassService.getIconclassByNotation(this.notation).subscribe(async result => {
        if (!result) {
          this.handleError();
          return;
        }
        this.iconclassData = result;
        this.hierarchy = [this.iconclassData];

        this.iconclassService.getIconclassListByNotation(this.iconclassData.parents.map(value => value + '')).subscribe(async res => {
          this.parents = res;
          this.hierarchy = this.parents.concat(this.iconclassData);
        });
        this.iconclassService.getIconclassListByNotation(this.iconclassData.children.map(value => value + '')).subscribe(async res => {
          this.children = res;
          this.hasIconographyChildren = this.children.length > 0;
        }, (() => {
          this.hasIconographyChildren = false;
        }));
      }, () => {
        this.notationExists = false;
      });
      
      /** load current page iconography slider items */
      this.sliderItemsCurrentIconography = await this.dataService.findArtworksByType(EntityType.ICONOGRAPHY, [this.notation]);
      this.sliderItemsCurrentIconography = this.sliderItemsCurrentIconography.filter(artwork => {
        return artwork.iconographies.find(iconography => iconography === this.notation);
      });

      if(this.sliderItemsCurrentIconography.length > 0) {
        this.sliderItemsCurrentIconography = shuffle(this.sliderItemsCurrentIconography);
        this.showCurrentIconographyArtworks = true;
      } else {
        this.showCurrentIconographyArtworks = false;  
      }
      
      /** load child iconography slider items */
      this.sliderItemsChildrenIconography = await this.dataService.findChildArtworksByIconography(this.notation, EntityType.ARTWORK);
      this.sliderItemsChildrenIconography = shuffle(this.sliderItemsChildrenIconography);
    });
  }

  /**
   * @description Hook that is called when a directive, pipe, or service is destroyed.
   */
  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  public handleError() {
    console.log('ERROR');
  }
}
