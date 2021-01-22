import { Component, OnInit, Input } from '@angular/core';
import { Artwork, Measurement } from '../../models/models';

@Component({
  selector: 'app-dimensions',
  templateUrl: './dimensions.component.html',
  styleUrls: ['./dimensions.component.scss']
})
export class DimensionsComponent implements OnInit {
  @Input() artwork: Artwork;
  /**
   * @description displays the dimensions of the artwork.
   */
  dimensionValue: string;

  /**
   * @description displays the label of the artwork dimensions.
   */
  dimensionLabel: string;

  /**
   * @description indicates the height of the illustration.
   */
  illustrationHeight: number;

  /**
   * @description indicates the width of the illustration.
   */
  illustrationWidth: number;

  /**
   * @description hides/shows illustration.
   */
  hideIllustration = false;

  measurement: Measurement;

  constructor() {
  }

  ngOnInit() {
    if (this.artwork) {
      this.measurement = this.artwork.measurements.find(m => {
        return (m.displayName.includes('Höhe') || m.displayName.includes('Breite') ||
          m.displayName.includes('Tiefe')) && m.displayName.includes(':');
      });
      this.setDimensions();
      this.setIllustrationDimensions();
    }
  }

  setDimensions() {
    if (this.measurement.diameter) {
      this.dimensionLabel = 'Diameter';
      /* Displays units if available. If not cm will be displayed */
      this.dimensionValue = this.measurement.diameter + (this.measurement.unit ? ' ' + this.measurement.unit : ' cm');
    } else if (this.measurement.height || this.measurement.width || this.measurement.length) {
      if (
        (this.measurement.height && this.measurement.width) ||
        (this.measurement.height && this.measurement.length) ||
        (this.measurement.width && this.measurement.length)
      ) {
        this.dimensionLabel = 'Dimension';
      } else if (this.measurement.height) {
        this.dimensionLabel = 'Height';
      } else if (this.measurement.width) {
        this.dimensionLabel = 'Width';
      } else if (this.measurement.length) {
        this.dimensionLabel = 'Length';
      }

      /* Displays units if available. If not cm will be displayed */

      if (
        (this.measurement.height && this.measurement.width && this.measurement.unit !== this.measurement.unit) ||
        (this.measurement.height && this.measurement.length && this.measurement.unit !== this.measurement.unit) ||
        (this.measurement.width && this.measurement.length && this.measurement.unit !== this.measurement.unit)
      ) {
        this.dimensionValue = [
          this.measurement.height ? this.measurement.height + (this.measurement.unit ? ' ' + this.measurement.unit : ' cm') : '',
          this.measurement.width ? this.measurement.width + (this.measurement.unit ? ' ' + this.measurement.unit : ' cm') : '',
          this.measurement.length ? this.measurement.length + (this.measurement.unit ? ' ' + this.measurement.unit : ' cm') : ''
        ]
          .filter(x => x)
          .join(' x ');
      } else {
        this.dimensionValue =
          [
            this.measurement.height ? this.measurement.height : '',
            this.measurement.width ? this.measurement.width : '',
            this.measurement.length ? this.measurement.length : ''
          ]
            .filter(x => x)
            .join(' x ') +
          ' ' +
          (this.measurement.height
            ? this.measurement.unit
            : this.measurement.width
              ? this.measurement.unit
              : this.measurement.length
                ? this.measurement.unit
                : 'cm');
      }
    }
  }

  setIllustrationDimensions() {
    // TODO: Refactor
    this.measurement.type = this.measurement.displayName.split(':')[0];
    this.measurement.unit = this.measurement.displayName.split(' ')[-1];
    this.measurement.value = this.measurement.displayName.substr(this.measurement.displayName.match('[dsx]*').index,
      this.measurement.unit.length);
    this.measurement.height = this.measurement.value.split('x')[0];
    this.measurement.width = this.measurement.value.split('x')[1];
    this.illustrationHeight = this.calculateIllustrationDimension(this.measurement.unit, this.measurement.height);
    this.illustrationWidth = this.calculateIllustrationDimension(this.measurement.unit, this.measurement.width);
    // Hide Dimension Illustration if Artwork is smaller than 9cm x 9cm or bigger than 35m
    if (this.illustrationHeight > 1855 || (this.illustrationHeight < 5 && this.illustrationWidth < 5)) {
      this.hideIllustration = true;
    }
  }

  calculateIllustrationDimension(dimensionUnit, dimension) {
    if (!dimension) {
      return 0;
    }
    const scalingFactor = 0.53;
    switch (dimensionUnit) {
      case 'ft':
        return scalingFactor * 30.48 * dimension;
      case 'm':
        return scalingFactor * 100 * dimension;
      case 'cm':
        return scalingFactor * dimension;
      case 'mm':
        return (scalingFactor / 10) * dimension;
      case 'in':
        return scalingFactor * dimension * 2.54;
      default:
        return 0;
    }
  }
}
