import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DataService } from 'src/app/core/services/elasticsearch/data.service';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TimelineComponent } from './timeline.component';
import { Ng5SliderModule } from 'ng5-slider';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { EntityType, EntityIcon } from '../../models/models';

describe('SliderComponent', () => {
  let component: TimelineComponent;
  let fixture: ComponentFixture<TimelineComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [NgbModule, Ng5SliderModule, HttpClientModule, RouterModule.forRoot([]), BrowserAnimationsModule],
      declarations: [TimelineComponent],
      providers: [DataService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimelineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create without items', () => {
    expect(component).toBeTruthy();
  });

  it('should create with items', () => {
    component.items = [
      {
        id: 'Q18578798',
        label: 'The Execution of the Four Crowned Martyrs',
        type: EntityType.ARTWORK,
        icon: EntityIcon.ARTWORK,
        route: '',
        count: 37,
        rank: 0.9795063116489386,
        date: 1300
      },
      {
        id: 'Q549172',
        label: 'Flight into Egypt',
        type: EntityType.ARTWORK,
        icon: EntityIcon.ARTWORK,
        route: '',
        count: 46,
        rank: 0.9944890206318238,
        date: 1305
      },
      {
        id: 'Q979440',
        label: 'Annunciation with St. Margaret and St. Ansanus',
        type: EntityType.ARTWORK,
        icon: EntityIcon.ARTWORK,
        route: '',
        count: 36,
        rank: 0.9762525340301427,
        date: 1333
      },
      {
        id: 'Q3815314',
        label: 'Head of Christ',
        type: EntityType.ARTWORK,
        icon: EntityIcon.ARTWORK,
        route: '',
        count: 21,
        rank: 0.22987683344390347,
        date: 1352
      }
    ];
    expect(component).toBeTruthy();
  });
});
