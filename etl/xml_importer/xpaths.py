namespace = {'lido': 'http://www.lido-schema.org'}

paths = {
    #ARTWORK
    "Artwork_Id_Path": 'lido:lidoRecID[@lido:source]',
    "Artwork_Name_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="preferred"][1]',
    "Artwork_Inception_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventDate/lido:displayDate',
    #entityTape?
    #inception?

    ##Prio 2
    "Artwork_Altename_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="alternative"]',
    "Artwork_Inscription_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:inscriptionsWrap/lido:inscriptions/lido:inscriptionDescription/lido:descriptiveNoteValue',

    #TYPE
    "Artwork_Type_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:objectWorkTypeWrap/lido:objectWorkType',
    "Type_ID_Path": 'lido:conceptID[@lido:source]',
    #"Type_EntityType_Path": 'is a simple string named "type"',
    "Type_Label_Path": 'lido:term[not(@lido:addedSearchTerm)]',
    "Type_AltLabel_Path": 'lido:term[@lido:addedSearchTerm="yes"]',
    #"Type_Source_Path": 'same path like 'Artwork_Type_Path''
    #"Type_Source_Id_Path": 'same path like 'Type_ID_Path''
    #"Type_Source_Source_Path": 'same path like 'Type_ID_Path''
    #"Type_Source_Term_Path": 'same path like 'Type_Name_Path''

    ##Prio 2
    #altNames

    # LOCATION
    "Artwork_Location_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet',
    "Location_Label_Path": 'lido:repositoryName/lido:legalBodyName/lido:appellationValue',

    "Location_PlaceID_Path": 'lido:repositoryLocation/lido:placeID[@lido:source]',
    "Location_Name_Path": 'lido:repositoryLocation/lido:namePlaceSet/lido:appellationValue',##Name und alte_Name haben gleuchen Path
    "Location_Altname_Path": 'lido:repositoryLocation/lido:namePlaceSet/lido:appellationValue',

    "Location_PlaceLabel_Path": 'lido:repositoryLocation/lido:namePlaceSet/lido:appellationValue',##hat gleiche Name mit Location_Name_Path

    #GENRE
    "Artwork_Genre_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:classificationWrap/lido:classification',
    "Genre_ID_Path": 'lido:conceptID[@lido:source]',
    "Genre_Label_Path": 'lido:term',
    "Genre_Altname_Path": 'lido:term[@lido:addedSearchTerm="yes"]',
    "Genre_ClassificationType": '[@lido:type]',


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
    "Artist_ID_Path": 'lido:actorInRole/lido:actor/lido:actorID[@lido:source]',
    "Artist_Name_Path": 'lido:actorInRole/lido:actor/lido:nameActorSet/lido:appellationValue[@lido:pref="preferred"]',
    "Artist_Altname_Path": 'lido:actorInRole/lido:actor/lido:nameActorSet/lido:appellationValue[not(@lido:pref="preferred")]',
    "Artist_Birth_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:earliestDate[@lido:type="birthDate"]',
    "Artist_Death_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:latestDate[@lido:type="deathDate"]',
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
    "Artwork_Materials_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventMaterialsTech',
    "Material_ID_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:conceptID[@lido:source]',
    "Material_name_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:term',
    "Material_Altname_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:term[@lido:addedSearchTerm="yes"]',
    #id
    #entityType
    #conceptID
    #name

    ##Prio 2
    #altNames

    #ICONOGRAPHY
    "Artwork_Iconographies_Path": 'lido:descriptiveMetadata/lido:objectRelationWrap/lido:subjectWrap/lido:subjectSet/lido:subject[@lido:type="Beschreibung"]',
    "Iconography_Id_Path": 'lido:subjectConcept/lido:conceptID[@lido:source]',
    "Iconography_Label_Path": 'lido:subjectConcept/lido:term[@lido:pref="preferred"]',
    "Iconography_Alt_Label_Path": 'lido:subjectConcept/lido:term',
    "Iconography_Iconclass_Path": 'lido:subjectConcept/lido:term[last()]',

    #id
    #entityType
    #conceptID
    #name

    ##Prio 2
    #altNames

    #MEASUREMENT
    "Artwork_Measurements_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet',
    "Measurement_DisplayName_Path": 'lido:displayObjectMeasurements',

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
    "RecordLegal_RecordID_Path": 'lido:recordID[@lido:source]',
    "RecordLegal_Rights_Path": 'lido:recordRights',
    "RecordType_ID_Path": 'lido:recordType/lido:conceptID',
    "RecordType_Term_Path": 'lido:recordType/lido:term',
    "RecordLegal_Source_Path": 'lido:recordSource/lido:legalBodyName/lido:appellationValue',
    "RecordLegal_RecordInfoLink_Path": 'lido:recordInfoSet/lido:recordInfoLink',

    #RESOURCE
    "Artwork_Resource_Path": 'lido:administrativeMetadata/lido:resourceWrap/lido:resourceSet',
    "Resource_resourceID_Path": 'lido:resourceID',
    "Resource_resourceType_Path": 'lido:resourceType/lido:term',
    "Resource_Rights_Path": 'lido:rightsResource',
    "Resource_ResourceDateTaken_Path": 'lido:resourceDateTaken/lido:displayDate',
    "Resource_LinkResource_Path": 'lido:resourceRepresentation/lido:linkResource',
    "Resource_Photographer_Path": 'lido:resourceSource[@lido:type="Fotograf"]/lido:legalBodyName/lido:appellationValue',



    #RIGHTS
    "Rights_Type_Path": "lido:rightsType/lido:conceptID",
    "Rights_Holder_Path": "lido:rightsHolder/lido:legalBodyID",
    #rightsHolder

    #ENTITY
    ##Prios sind niedrig oder nicht vorhanden, daher erstmal nicht beachten

    "namespace": "{'lido': 'http://www.lido-schema.org'}"
}

