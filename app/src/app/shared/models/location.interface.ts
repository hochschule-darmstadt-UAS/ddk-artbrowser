import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Location extends Entity {
  inventoryNumber?: string;
  placeName?: string;
  placeAltNames?: string[];
  part_of: Partial<Location>[];
  type: EntityType.LOCATION;
  icon: EntityIcon.LOCATION;
}
