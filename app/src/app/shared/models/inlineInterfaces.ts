export interface SourceID {
  source: string;
  id: string;
  term?: string;
  label?: string;
}

export interface Rights {
  rightsType: SourceID;
  rightsHolder: SourceID;
}

export interface Resource {
  resourceID: SourceID[];
  resourceType: string;
  rights: Rights;
  description: string;
  photographer: string;
  dateTaken: string;
  linkResource: string;
  imageSmall: string;
  imageMedium: string;
  image: string;
  error: boolean; // used to mark loading errors
}

export interface RecordLegal {
  recordID: SourceID[];
  recordType: SourceID[];
  recordSource: string;
  rights: Rights;
  recordInfoLink: string[];
}

export interface Measurement {
  displayName?: string;
  type?: string;
  unit?: string;
  value?: string;
  extend?: string;
  shape?: string;
  format?: string;
  qualifier?: string;
  height?: string; // util
  width?: string; // util
  length?: string; // util
  diameter?: string; // util
}
