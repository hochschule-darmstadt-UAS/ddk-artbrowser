import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Material extends Entity {
  entityType: EntityType.MATERIAL;
  icon: EntityIcon.MATERIAL;
}
