import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WrongIdComponent } from './wrong-id.component';

describe('WrongIdComponent', () => {
  let component: WrongIdComponent;
  let fixture: ComponentFixture<WrongIdComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WrongIdComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WrongIdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
