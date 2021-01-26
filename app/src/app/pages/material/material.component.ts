import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { Material, Artwork, EntityType } from 'src/app/shared/models/models';
import { Subject } from 'rxjs';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { shuffle } from 'src/app/core/services/utils.service';

@Component({
  selector: 'app-material',
  templateUrl: './material.component.html',
  styleUrls: ['./material.component.scss']
})
export class MaterialComponent implements OnInit, OnDestroy {
  /** use this to end subscription to url parameter in ngOnDestroy */
  private ngUnsubscribe = new Subject();

  /** The entity this page is about */
  material: Material = null;

  /** Related artworks */
  sliderItems: Artwork[] = [];

  idDoesNotExist = false;
  materialId: string;

  constructor(private dataService: DataService, private route: ActivatedRoute) {}

  /** hook that is executed at component initialization */
  ngOnInit() {
    /** Extract the id of entity from URL params. */
    this.route.paramMap.pipe(takeUntil(this.ngUnsubscribe)).subscribe(async params => {
      this.materialId = params.get('materialId');

      /** Use data service to fetch entity from database */
      this.material = await this.dataService.findById<Material>(this.materialId, EntityType.MATERIAL);

      if (!this.material) {
        this.idDoesNotExist = true;
        return;
      }

      /** load slider items */
      this.dataService.findArtworksByType(EntityType.MATERIAL, [this.material.id]).then(artworks => (this.sliderItems = shuffle(artworks)));
    });
  }

  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }
}
