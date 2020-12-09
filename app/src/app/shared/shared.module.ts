import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CarouselComponent } from './components/carousel/carousel.component';
import { SlideComponent } from './components/carousel/slide/slide.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import { SearchComponent } from './components/search/search.component';
import { FormsModule } from '@angular/forms';
import { InformationComponent } from './components/information/information.component';
import { AbstractComponent } from './components/abstract/abstract.component';
import { TitleComponent } from './components/title/title.component';
import { IconclassComponent } from './components/iconclass/iconclass.component';
import { BadgeComponent } from './components/badge/badge.component';
import { TimelineComponent } from './components/timeline/timeline.component';
import { CollapseComponent } from './components/collapse/collapse.component';
import { Angulartics2Module } from 'angulartics2';
import { NgxFitTextModule } from 'ngx-fit-text';
import { DimensionsComponent } from './components/dimensions/dimensions.component';
import { InfiniteScrollComponent } from './components/infinite-scroll/infinite-scroll.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider';

/** Everything that should be used within multiple feature modules but isn't always required goes here */
@NgModule({
  declarations: [
    CarouselComponent,
    SlideComponent,
    SearchComponent,
    TimelineComponent,
    BadgeComponent,
    TitleComponent,
    InformationComponent,
    AbstractComponent,
    IconclassComponent,
    CollapseComponent,
    DimensionsComponent,
    InfiniteScrollComponent,
    CollapseComponent
  ],
  imports: [CommonModule, NgbModule, RouterModule, FormsModule, NgxSliderModule, Angulartics2Module, NgxFitTextModule],
  exports: [
    CarouselComponent,
    SearchComponent,
    TimelineComponent,
    BadgeComponent,
    NgbModule,
    TitleComponent,
    InformationComponent,
    AbstractComponent,
    IconclassComponent,
    CollapseComponent,
    DimensionsComponent,
    CollapseComponent,
    InfiniteScrollComponent
  ]
})
export class SharedModule {}
