import { SourceID } from './utils';

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
  sourceID?: Partial<SourceID>[];
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
  TYPE = 'type',
}

export const usePlural = (type: EntityType) => (type === 'all' ? type : type === EntityType.ICONOGRAPHY ? 'iconographies' : type + 's');
export const usePluralAttributes = (type: EntityType) =>
  type === 'all' ? type : type === EntityType.ICONOGRAPHY ? 'iconographies' : type === EntityType.LOCATION ? 'location' : type + 's';

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
