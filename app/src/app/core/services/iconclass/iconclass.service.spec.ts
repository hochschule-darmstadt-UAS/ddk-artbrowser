import { async, TestBed } from '@angular/core/testing';
import { IconclassService } from './iconclass.service';
import { HttpClientModule } from '@angular/common/http';

describe('IconclassService', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ]
    }).compileComponents();
  }));

  it('should be created', () => {
    const service: IconclassService = TestBed.get(IconclassService);
    expect(service).toBeTruthy();
  });
});
