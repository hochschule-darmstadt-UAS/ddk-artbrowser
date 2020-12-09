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

