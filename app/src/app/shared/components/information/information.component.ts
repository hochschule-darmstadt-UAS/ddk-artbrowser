import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Entity } from '../../models/models';
import { SourceID } from '../../models/inlineInterfaces';
import { SourceToLabel } from '../../../core/services/ddk.service';

@Component({
  selector: 'app-information',
  templateUrl: './information.component.html',
  styleUrls: ['./information.component.scss']
})
export class InformationComponent implements OnChanges {
  @Input()
  label: string;

  @Input()
  value: string;

  @Input()
  isHref: boolean;

  @Input()
  values: Entity[];

  @Input()
  sourceID: SourceID[];

  constructor() {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.sourceID) {
      this.handleSourceIDArray(changes.sourceID.currentValue);
    }
    this.checkRequiredFields();
  }

  /**
   * This Method sets the label of sourceID
   */
  handleSourceIDArray(sIDs: SourceID[]) {
    sIDs.filter(sID => Object.keys(SourceToLabel).includes(sID.source)).map(sID => sID.label = SourceToLabel[sID.source]);
  }

  /**
   * This Method is for debugging purposes.
   * Errors will not be shown in productive state.
   */
  private checkRequiredFields() {
    if (this.label === null) {
      throw new TypeError('Attribute \'label\' is required');
    }
  }
}
