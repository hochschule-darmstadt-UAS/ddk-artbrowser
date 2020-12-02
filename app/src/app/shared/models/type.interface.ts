import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Type extends Entity {
  type: EntityType.TYPE;
  icon: EntityIcon.TYPE;
}
