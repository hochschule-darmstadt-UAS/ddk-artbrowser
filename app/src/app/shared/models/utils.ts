export interface SourceID {
  source: string;
  id: string;
  term?: string;
}

export interface Rights {
  rightsType: SourceID;
  rightsHolder: SourceID;
}

export interface Resource {
  resourceID: SourceID[];
  resourceType: string;
  rights: Rights;
  photographer: string;
  dateTaken: string;
  linkResource: string;
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
