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

const prefix = 'http://www.bildindex.de/bilder/';
export const image = (linkResource) => {
  const imageID = linkResource.substr(linkResource.lastIndexOf('/') + 1);
  return linkResource ? prefix + 'd/' + imageID : null;
};
export const imageMedium = (linkResource) => {
  const imageID = linkResource.substr(linkResource.lastIndexOf('/') + 1);
  return linkResource ? prefix + 'm/' + imageID : null;
};
export const imageSmall = (linkResource) => {
  const imageID = linkResource.substr(linkResource.lastIndexOf('/') + 1);
  return linkResource ? prefix + 't/' + imageID : null;
};

export enum SourceToLabel {
  'http://vocab.getty.edu/ulan' = 'Union List of Artist Names ID',
  'http://vocab.getty.edu/tgn' = 'Getty Thesaurus of Geographic Names ID',
  'http://vocab.getty.edu/aat' = 'Art & Architecture Thesaurus ID',
  'ISIL (ISO 15511)' = 'International Standard Identifier for Libraries and Related Organizations (ISIL)',
  'http://d-nb.info/gnd' = 'German National Library ID'
}
