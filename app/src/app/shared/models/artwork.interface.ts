import { Entity, EntityIcon, EntityType } from './entity.interface';
import { Artist } from './artist.interface';
import { Genre } from './genre.interface';
import { Material } from './material.interface';
import { Iconography } from './iconography.interface';
import { Measurement, RecordLegal, Resource } from './inlineInterfaces';
import { Type } from './type.interface';

export interface Artwork extends Entity {
  artists: Partial<Artist>[];
  locations: Partial<Location>[];
  genres: Partial<Genre>[];
  types: Partial<Type>[];
  iconographies: Partial<Iconography>[];
  materials: Partial<Material>[];
  measurements: Partial<Measurement>[];
  recordLegal: Partial<RecordLegal>;
  resources: Partial<Resource>[];
  inscriptions?: string[];
  inception?: number;
  entityType: EntityType.ARTWORK;
  icon: EntityIcon.ARTWORK;
}
