import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Genre extends Entity {
  classificationType?: string;
  entityType: EntityType.GENRE;
  icon: EntityIcon.GENRE;
}
