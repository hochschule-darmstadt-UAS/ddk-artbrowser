import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { Subject } from 'rxjs';
import { IconclassService } from '../../core/services/iconclass/iconclass.service';
import { Iconography } from '../../shared/models/iconography.interface';
import { Entity } from '../../shared/models/entity.interface';

@Component({
  selector: 'app-iconography',
  templateUrl: './iconography.component.html',
  styleUrls: ['./iconography.component.scss']
})
export class IconographyComponent implements OnInit {
  notation: string;
  iconclassData: Iconography;
  hierarchy: Entity[];

  children: Iconography[] = [];
  parents: Iconography[] = [];

  private appInfoRef: ElementRef;
  /**
   * @description use this to end subscription to url parameter in ngOnDestroy
   */
  private ngUnsubscribe = new Subject();

  constructor(private iconclassService: IconclassService, private route: ActivatedRoute) {}

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
        });
      });
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
