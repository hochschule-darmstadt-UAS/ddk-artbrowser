import { Component, OnInit, Input } from '@angular/core';
import { Entity } from '../../models/models';
import { SourceID } from '../../models/utils';

@Component({
  selector: 'app-information',
  templateUrl: './information.component.html',
  styleUrls: ['./information.component.scss']
})
export class InformationComponent {
  @Input()
  label: string;

  @Input()
  value: string;

  @Input()
  isHref: boolean;

  @Input()
  values: Entity[];

  @Input()
  sourceID: Partial<SourceID>[];

  constructor() {}

  ngOnChanges() {
    this.checkRequiredFields();
  }

  /**
   * This Method is for debugging purposes.
   * Errors will not be shown in productive state.
   */
  private checkRequiredFields() {
    if (this.label === null) {
      throw new TypeError("Attribute 'label' is required");
    }
  }
}
