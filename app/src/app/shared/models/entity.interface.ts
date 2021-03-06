import { SourceID } from './inlineInterfaces';

export interface Entity {
  id: string;
  label?: string;
  altLabels?: string[];
  image?: string;
  imageSmall?: string;
  imageMedium?: string;
  entityType: EntityType;
  icon: EntityIcon;
  count: number;
  rank: number;
  route: string;
  sourceIDs?: Partial<SourceID>[];
}

export type Iconclass = string;

export enum EntityType {
  ALL = 'all',
  ARTIST = 'artist',
  ARTWORK = 'artwork',
  GENRE = 'genre',
  LOCATION = 'location',
  MATERIAL = 'material',
  MOVEMENT = 'movement',
  ICONOGRAPHY = 'iconography',
  TYPE = 'type',
}

export const usePlural = (type: EntityType) => (type === 'all' ? type : type === EntityType.ICONOGRAPHY ? 'iconographies' : type + 's');

export enum EntityIcon {
  ALL = 'fa-list-ul',
  ARTIST = 'fa-user',
  ARTWORK = 'fa-image',
  LOCATION = 'fa-archway',
  GENRE = 'fa-tag',
  TYPE = 'fa-shapes',
  MATERIAL = 'fa-scroll',
  ICONOGRAPHY = 'fa-fingerprint',
}
