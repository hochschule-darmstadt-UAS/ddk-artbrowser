import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtworkComponent } from './artwork.component';
import { SlideComponent } from 'src/app/shared/components/carousel/slide/slide.component';
import { CarouselComponent } from 'src/app/shared/components/carousel/carousel.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { ImageViewerModule } from 'ngx-image-viewer';
import { RouterModule } from '@angular/router';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { BadgeComponent } from 'src/app/shared/components/badge/badge.component';
import { CollapseComponent } from 'src/app/shared/components/collapse/collapse.component';
import { InformationComponent } from '../../shared/components/information/information.component';
import { TitleComponent } from 'src/app/shared/components/title/title.component';
import { DimensionsComponent } from 'src/app/shared/components/dimensions/dimensions.component';
import { NgImageSliderModule } from 'ng-image-slider';

describe('ArtworkComponent', () => {
  let component: ArtworkComponent;
  let fixture: ComponentFixture<ArtworkComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [NgbModule,
        HttpClientModule,
        ImageViewerModule.forRoot(),
        RouterModule.forRoot([]),
        NgImageSliderModule],
      declarations: [
        ArtworkComponent,
        SlideComponent,
        BadgeComponent,
        CarouselComponent,
        TitleComponent,
        InformationComponent,
        DimensionsComponent,
        CollapseComponent
      ],
      providers: [DataService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArtworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
