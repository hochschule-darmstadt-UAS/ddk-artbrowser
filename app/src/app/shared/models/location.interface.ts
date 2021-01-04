import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Location extends Entity {
  inventoryNumber?: string;
  placeLabel?: string;
  placeAltLabels?: string[];
  part_of: Partial<Location>[];
  entityType: EntityType.LOCATION;
  icon: EntityIcon.LOCATION;
}
