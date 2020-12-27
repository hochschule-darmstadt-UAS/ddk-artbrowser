import { Entity, EntityIcon, EntityType } from './entity.interface';

export interface Artist extends Entity {
  gender?: 'male' | 'female';
  dateOfBirth?: string;
  dateOfDeath?: string;
  evidenceFirst?: string;
  evidenceLast?: string;
  nationality?: string;
  roles: string[];
  entityType: EntityType.ARTIST;
  icon: EntityIcon.ARTIST;
}
