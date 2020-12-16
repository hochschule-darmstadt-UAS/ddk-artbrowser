/**
 * TODO: Move to Data Import
 * Possible Strings:
 * 17. Jahrhundert
 * 2. Hälfte 17. Jahrhundert
 * letztes Viertel 18. Jahrhundert
 * 3. Viertel 13. Jahrhundert
 * letztes Drittel 18. Jahrhundert
 * 2. Drittel 18. Jahrhundert
 * Anfang 15. Jahrhundert
 * Ende 18. Jahrhundert
 * nach 700
 * um 1920/1940?
 * vor 1653
 * ab 1730
 * um 1200 &amp; 1277-1324 &amp; 1466 &amp; ab 1694 &amp; 1819
 * @param dateString: date in random string format
 * @returns number of minimal year in dateString
 */
export const getYearFromString = (dateString: string): number | string => {
  const splitDate = dateString.split(' ');
  if (dateString.match('\\d+\\. Jahrhundert')) {
    if (dateString.match('\\d\\. Hälfte \\d+\\. Jahrhundert')) {
      return (parseInt(splitDate[0], 10) - 1) * 50 + 25 + (parseInt(splitDate[2], 10) - 1) * 100;
    } else if (dateString.match('\\d\\. Viertel \\d+\\. Jahrhundert')) {
      return (parseInt(splitDate[0], 10) - 1) * 25 + 12 + (parseInt(splitDate[2], 10) - 1) * 100;
    } else if (dateString.match('letztes Viertel \\d+\\. Jahrhundert')) {
      return 3 * 25 + 12 + (parseInt(splitDate[2], 10) - 1) * 100;
    } else if (dateString.match('\\d\\. Drittel \\d+\\. Jahrhundert')) {
      return (parseInt(splitDate[0], 10) - 1) * 33 + 16 + (parseInt(splitDate[2], 10) - 1) * 100;
    } else if (dateString.match('letztes Drittel \\d+\\. Jahrhundert')) {
      return 2 * 33 + 16 + (parseInt(splitDate[2], 10) - 1) * 100;
    } else if (dateString.match('Anfang \\d+\\. Jahrhundert')) {
      return (parseInt(splitDate[1], 10) - 1) * 100 + 1;
    } else if (dateString.match('Ende \\d+\\. Jahrhundert')) {
      return (parseInt(splitDate[1], 10)) * 100;
    } else {
      return (parseInt(splitDate[0], 10) - 1) * 100 + 1;
    }
  } else if (dateString.match('nach \\d+')) {
    return (parseInt(splitDate[1], 10) + 1);
  } else if (dateString.match('um \\d+')) {
    return (parseInt(splitDate[1], 10));
  } else if (dateString.match('vor \\d+')) {
    return (parseInt(splitDate[1], 10) - 1);
  } else if (dateString.match('ab \\d+')) {
    return (parseInt(splitDate[1], 10) + 1);
  }
  return dateString.match('\\d+') ? parseInt(dateString.match('\\d+')[0], 10) : dateString;
};

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
