import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TypeComponent } from './type.component';
import { SlideComponent } from 'src/app/shared/components/carousel/slide/slide.component';
import { CarouselComponent } from 'src/app/shared/components/carousel/carousel.component';
import { WrongIdComponent } from 'src/app/shared/components/wrong-id/wrong-id.component';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { TitleComponent } from 'src/app/shared/components/title/title.component';
import { InformationComponent } from 'src/app/shared/components/information/information.component';
import { BadgeComponent } from 'src/app/shared/components/badge/badge.component';
import { CollapseComponent } from 'src/app/shared/components/collapse/collapse.component';

describe('MotifComponent', () => {
  let component: TypeComponent;
  let fixture: ComponentFixture<TypeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [NgbModule, HttpClientModule, RouterModule.forRoot([])],
      declarations: [
        TypeComponent,
        SlideComponent,
        CarouselComponent,
        BadgeComponent,
        CollapseComponent,
        TitleComponent,
        InformationComponent,
        WrongIdComponent
      ],
      providers: [DataService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
