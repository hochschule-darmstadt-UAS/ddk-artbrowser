import { Inject, Injectable, LOCALE_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { iconclassEnvironment } from '../../../../environments/environment';
import { Observable, throwError } from 'rxjs';
import { Iconography } from '../../../shared/models/iconography.interface';
import 'rxjs/add/operator/map';
import { EntityIcon, EntityType } from '../../../shared/models/entity.interface';

@Injectable({
  providedIn: 'root'
})
export class IconclassService {
  private readonly ISO_639_1_LOCALE: string;

  constructor(private http: HttpClient, @Inject(LOCALE_ID) localeId: string) {
    // build backend api url with specific index by localeId
    this.ISO_639_1_LOCALE = localeId.substr(0, 2);
  }

  public getIconclassByNotation(notation: string): Observable<Iconography> {
    return this.getIconclassListByNotation([notation]).map(value => {
      if (value.length > 0) {
        return value[0];
      } else {
        return;
      }
    });
  }

  public getIconclassListByNotation(notations: string[]): Observable<Iconography[]> {
    notations = notations.map(notation => encodeURI(notation));
    console.log(notations);
    const uri = iconclassEnvironment.apiURI + '/?notation=' + notations.join('&notation=');
    console.log(uri);
    return this.http.get(uri).map((response: Array<any>) => {
      if (!response.length) {
        throw throwError('Response was empty!');
      }
      return response.map(item => {
        const ico = {
          id: item.n,
          icon: EntityIcon.ICONOGRAPHY,
          type: EntityType.ICONOGRAPHY,
          children: item.c,
          parents: item.p,
          keywords: item.kw,
          text: item.txt
        } as Iconography;
        this.setIconographyLabel(ico);
        return ico;
      });
    });
  }

  public setIconographyLabel(iconography: Iconography) {
    const regex = /[();]/g; // TODO: find better regex?
    const match = regex.exec(iconography.text[this.ISO_639_1_LOCALE || 'de']); // TODO: substitute with active language
    if (match) {
      iconography.label = iconography.id + ': ' + iconography.text[this.ISO_639_1_LOCALE || 'de'].substr(0, match.index);
    } else {
      iconography.label = iconography.id + ': ' + iconography.text[this.ISO_639_1_LOCALE || 'de'];
    }
    iconography.label = iconography.label.length > 50 ? iconography.label.substr(0, 50) + '...' : iconography.label;
    iconography.text[this.ISO_639_1_LOCALE || 'de'] = this.capitalizeFirstLetter(iconography.text[this.ISO_639_1_LOCALE || 'de']);
    return iconography;
  }

  private capitalizeFirstLetter(iconText: string) {
    return iconText.charAt(0).toUpperCase() + iconText.slice(1);
  }
}