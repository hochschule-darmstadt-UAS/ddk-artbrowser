import { Component, Input, SimpleChanges } from '@angular/core';
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
  sourceID: SourceID[];

  sourceIDObject: any;

  constructor() {}

  ngOnChanges(changes: SimpleChanges) {
    if(changes.sourceID) {
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
  handleSourceIDArray(sID: SourceID[]) {
    this.sourceIDObject = { ...sID };
    for (let key in this.sourceIDObject) {
      if(this.sourceIDObject[key].source.includes("vocab.getty.edu")) {
        this.sourceIDObject['getty'] = this.sourceIDObject[key];
        delete this.sourceIDObject[key];
      } else {
        if(this.sourceIDObject[key].source.includes("d-nb.info")) {
          this.sourceIDObject['dnb'] = this.sourceIDObject[key];
          delete this.sourceIDObject[key];
        }
      }
    }
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
