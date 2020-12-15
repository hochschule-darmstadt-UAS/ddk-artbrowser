import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Entity } from '../../models/models';
import { SourceID, SourceToLabel } from '../../models/utils';

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

  sourceIDObject: any;

  constructor() {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.sourceID) {
      this.handleSourceIDArray(changes.sourceID.currentValue);
    }
    this.checkRequiredFields();
  }

  /**
   * This Method converts sourceID Array to an object and checks
   * if the element is a getty- or dnb-element and 'renames'
   * the key to getty or dnb. These keys are checked inside
   * the html-template
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
