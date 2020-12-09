import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ArtistComponent } from './artist.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import { SlideComponent } from 'src/app/shared/components/carousel/slide/slide.component';
import { CarouselComponent } from 'src/app/shared/components/carousel/carousel.component';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { HttpClientModule } from '@angular/common/http';
import { BadgeComponent } from 'src/app/shared/components/badge/badge.component';
import { TimelineComponent } from 'src/app/shared/components/timeline/timeline.component';
import { NgxSliderModule } from '@angular-slider/ngx-slider';
import { CollapseComponent } from 'src/app/shared/components/collapse/collapse.component';
import { TitleComponent } from 'src/app/shared/components/title/title.component';
import { InformationComponent } from 'src/app/shared/components/information/information.component';
import { AbstractComponent } from 'src/app/shared/components/abstract/abstract.component';

// TODO: we might want to have tests that actually test functionality
describe('ArtistComponent', () => {
  let component: ArtistComponent;
  let fixture: ComponentFixture<ArtistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [NgbModule, HttpClientModule, RouterModule.forRoot([]), NgxSliderModule],
      declarations: [
        ArtistComponent,
        SlideComponent,
        CarouselComponent,
        TimelineComponent,
        AbstractComponent,
        TitleComponent,
        InformationComponent,
        BadgeComponent,
        CollapseComponent
      ],
      providers: [DataService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArtistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
