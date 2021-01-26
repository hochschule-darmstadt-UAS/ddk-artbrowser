import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IconographyComponent } from './iconography.component';
import { BadgeComponent } from '../../shared/components/badge/badge.component';
import { CarouselComponent } from '../../shared/components/carousel/carousel.component';
import { TitleComponent } from '../../shared/components/title/title.component';
import { InformationComponent } from '../../shared/components/information/information.component';
import { CollapseComponent } from '../../shared/components/collapse/collapse.component';
import { WrongIdComponent } from 'src/app/shared/components/wrong-id/wrong-id.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { IconclassService } from '../../core/services/iconclass/iconclass.service';
import { SlideComponent } from '../../shared/components/carousel/slide/slide.component';
import { DataService } from '../../core/services/elasticsearch/data.service';

describe('IconographyComponent', () => {
  let component: IconographyComponent;
  let fixture: ComponentFixture<IconographyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [NgbModule, HttpClientModule, RouterModule.forRoot([])],
      declarations: [
        IconographyComponent,
        SlideComponent,
        BadgeComponent,
        CarouselComponent,
        TitleComponent,
        InformationComponent,
        CollapseComponent,
        WrongIdComponent
      ],
      providers: [IconclassService, DataService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IconographyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
