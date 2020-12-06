import { SourceID } from './utils';

export interface Entity {
  id: string;
  label?: string;
  image?: string;
  imageSmall?: string;
  imageMedium?: string;
  entityType: EntityType;
  icon: EntityIcon;
  count: number;
  rank: number;
  route: string;
  sourceID?: Partial<SourceID>;
  conceptID?: Partial<SourceID>[];
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
  MOTIF = 'motif',
  ICONOGRAPHY = 'iconography',
  TYPE = 'type'
}

export const usePlural = (type: EntityType) => (type === 'all' ? type : type + 's');

export enum EntityIcon {
  ALL = 'fa-list-ul',
  ARTIST = 'fa-user',
  ARTWORK = 'fa-image',
  LOCATION = 'fa-archway',
  GENRE = 'fa-tag',
  TYPE = 'fa-tag',
  MATERIAL = 'fa-scroll',
  ICONOGRAPHY = 'fa-fingerprint'
}
