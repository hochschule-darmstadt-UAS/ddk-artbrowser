paths = {
    #ARTWORK
    "Artwork_Id_Path": 'lido:lidoRecID[@lido:source]',
    "Artwork_Name_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="preferred"][1]',
    #entityTape?
    #inception?

    ##Prio 2
    "Artwork_Altename_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="alternative"]',
    "Artwork_Inscription_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:inscriptionsWrap/lido:inscriptions/lido:inscriptionDescription/lido:descriptiveNoteValue',

    #TYPE
    "Artwork_Type_ID_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:objectWorkTypeWrap/lido:objectWorkType/lido:conceptID[@lido:source]',
    #entityType
    "Artwork_Type_Name_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:objectWorkTypeWrap/lido:objectWorkType/lido:term',
    #conceptId

    ##Prio 2
    #altNames

    #GENRE
    "Artwork_Genres_ID_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:classificationWrap/lido:classification/lido:conceptID[@lido:source]',
    #id
    #type
    #name
    #conceptID
    #classificationType

    ##Prio 2
    #altNames

    #LOCATION
    "Artwork_Location_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet[1]/lido:repositoryName/lido:legalBodyName/lido:appellationValue[1]',
    #id
    #entityType
    #name
    #placeID
    #placeName

    ##Prio 2
    #inventoryNumber

    ##Prio 3
    #placeAltNames
    #altNames

    #ARTIST
    "Artwork_Artists_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventActor',
    #id
    #entityType
    #actorID
    #name
    #birth
    #death

    ##Prio 2
    #altNames  2
    #nationality  2
    #evidenceFirst  2
    #evidenceLast  2
    #gender  2
    #roles  2

    #MATERIAL
    #id
    #entityType
    #conceptID
    #name

    ##Prio 2
    #altNames

    #ICONOGRAPHY
    "Artwork_Iconographies_Path": 'lido:descriptiveMetadata/lido:objectRelationWrap/lido:subjectWrap/lido:subjectSet/lido:subject/lido:subjectConcept/lido:conceptID[@lido:source]',
    #id
    #entityType
    #conceptID
    #name

    ##Prio 2
    #altNames

    #MEASUREMENT
    "Artwork_Measurements_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet',
    "Artwork_Measurments_DisplaySize_Path": 'lido:displayObjectMeasurements',

    ##Prio 2
    "Artwork_Measurments_Type_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementType',
    "Artwork_Measurments_Unit_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementUnit',
    "Artwork_Measurments_Value_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementValue',
    "Artwork_Measurments_displayName_Path": 'lido:displayObjectMeasurements',
    "Artwork_Measurments_Shape_Path": 'lido:shapeObjectMeasurements',
    "Artwork_Measurments_Format_Path": 'lido:formatObjectMeasurements',
    "Artwork_Measurments_Qualifier_Path": 'lido:qualifierObjectMeasurements',

    #SOURCEID
    #source
    #id
    #term

    #RECORDLEGAL
    "Artwork_RecordLegal_Path": 'lido:administrativeMetadata/lido:recordWrap',
    "Artwork_RecordLegal_RecordID_Path": 'lido:recordID[@lido:source]',
    "Artwork_RecordLegal_RecordType_Path": 'lido:recordType',
    "Artwork_RecordLegal_RecordSource_Path": 'lido:recordSource',
    "Artwork_RecordLegal_Rights_Path": 'lido:recordRights',
    "Artwork_RecordLegal_RecordInfoLink_Path": 'lido:recordInfoSet/lido:recordInfoLink',

    #RESOURCE
    "Artwork_Resource_Path": 'lido:administrativeMetadata/lido:resourceWrap/lido:resourceSet',
    "Artwork_Resource_resourceID_Path": 'lido:resourceID',
    "Artwork_Resource_resourceType_Path": 'lido:resourceType/lido:term',
    "Artwork_Resource_Rights_Path": 'lido:rightsResource',
    #photographer
    "Artwork_Resource_ResourceDateTaken_Path": 'lido:resourceDateTaken/lido:displayDate',
    "Artwork_Resource_LinkResource_Path": 'lido:resourceRepresentation/lido:linkResource',

    #RIGHTS
    #rightsType
    #rightsHolder

    #ENTITY
    ##Prios sind niedrig oder nicht vorhanden, daher erstmal nicht beachten

    "namespace": "{'lido': 'http://www.lido-schema.org'}"
}

