paths = {
    #ARTWORK
    "Artwork_Id_Path": 'lido:lidoRecID[@lido:source]',

    "Artwork_Name_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="preferred"][1]',

    "Artwork_Measurements_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet',
    "Artwork_Mesurments_DisplaySize_Path": 'lido:displayObjectMeasurements',
    "Artwork_Mesurments_Type_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementType',
    "Artwork_Mesurments_Unit_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementUnit',
    "Artwork_Mesurments_Value_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementValue',
    "Artwork_Mesurments_displayName_Path": 'lido:displayObjectMeasurements',
    "Artwork_Mesurments_Shape_Path": 'lido:shapeObjectMeasurements',
    "Artwork_Mesurments_Format_Path": 'lido:formatObjectMeasurements',
    "Artwork_Mesurments_Qualifier_Path": 'lido:qualifierObjectMeasurements',

    "Artwork_Altename_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="alternative"]',

    "Artwork_RecordLegal_Path": 'lido:administrativeMetadata/lido:recordWrap',
    "Artwork_RecordLegal_RecordID_Path": 'lido:recordID[@lido:source]',
    "Artwork_RecordLegal_RecordType_Path": 'lido:recordType',
    "Artwork_RecordLegal_RecordSource_Path": 'lido:recordSource',
    "Artwork_RecordLegal_Rights_Path": 'lido:recordRights',

    "Artwork_RecordLegal_RecordInfoLink_Path": 'lido:recordInfoSet/lido:recordInfoLink',

    "Artwork_ResourceLegal_Path": 'lido:administrativeMetadata/lido:resourceWrap/lido:resourceSet',
    "Artwork_ResourceLegal_resourceID_Path": 'lido:resourceID',
    "Artwork_ResourceLegal_resourceType_Path": 'lido:resourceType/lido:term',
    "Artwork_ResourceLegal_Rights_Path": 'lido:rightsResource',
    "Artwork_ResourceLegal_ResourceDateTaken_Path": 'lido:resourceDateTaken/lido:displayDate',
    "Artwork_ResourceLegal_LinkResource_Path": 'lido:resourceRepresentation/lido:linkResource',

    "Artwork_Type_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:objectWorkTypeWrap/lido:objectWorkType/lido:conceptID[@lido:source]',

    "Artwork_Genres_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:classificationWrap/lido:classification/lido:conceptID[@lido:source]',

    "Artwork_Location_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet[1]/lido:repositoryName/lido:legalBodyName/lido:appellationValue[1]',

    "Artwork_Artists_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventActor',

    "Artwork_Iconographies_Path": 'lido:descriptiveMetadata/lido:objectRelationWrap/lido:subjectWrap/lido:subjectSet/lido:subject/lido:subjectConcept/lido:conceptID[@lido:source]',

    "Artwork_Inscription_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:inscriptionsWrap/lido:inscriptions/lido:inscriptionDescription/lido:descriptiveNoteValue',

    "namespace": "{'lido': 'http://www.lido-schema.org'}"

# LOCATION

# GENRE

# ARTIST

# MATERIAL

# ICONGRAPHYS


}

