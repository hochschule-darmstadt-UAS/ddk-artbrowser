import { Entity, EntityType } from './entity.interface';

export interface Iconography extends Entity {
  parents: Array<object>;
  children: Array<object>;
  keywords: object;
  text: IconographyText;
  entityType: EntityType.ICONOGRAPHY;
}

export interface IconographyText {
  fi: string;
  fr: string;
  de: string;
  en: string;
  it: string;
}
