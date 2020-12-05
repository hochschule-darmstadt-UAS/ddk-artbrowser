import { Component, OnInit, Input } from '@angular/core';
import { Entity } from '../../models/models';

@Component({
  selector: 'app-abstract',
  templateUrl: './abstract.component.html',
  styleUrls: ['./abstract.component.scss']
})
export class AbstractComponent implements OnInit {
  @Input()
  entity: Entity;

  constructor() {}

  ngOnInit() {
    this.checkRequiredFields();
  }

  /**
   * Check on every change if the preconditions are met
   */
  ngOnChanges(changes) {
    this.checkRequiredFields();
  }

  /**
   * This method checks if the required entity prop has been passed to the component
   */
  private checkRequiredFields() {
    if (this.entity === null) {
      throw new TypeError("Attribute 'entity' is required");
    }
  }
}
