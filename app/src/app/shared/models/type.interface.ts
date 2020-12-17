import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Type extends Entity {
  entityType: EntityType.TYPE;
  icon: EntityIcon.TYPE;
}
