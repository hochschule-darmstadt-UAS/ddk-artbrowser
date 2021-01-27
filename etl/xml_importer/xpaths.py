namespace = {'lido': 'http://www.lido-schema.org'}

paths = {
    #ARTWORK
    "Artwork_Id_Path": 'lido:lidoRecID[@lido:source]',
    "Artwork_Name_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="preferred"][1]',
    "Artwork_Inception_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventDate/lido:displayDate',

    ##Prio 2
    "Artwork_AltLabel_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="alternative"]',
    "Artwork_Inscription_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:inscriptionsWrap/lido:inscriptions/lido:inscriptionDescription/lido:descriptiveNoteValue',

    #TYPE
    "Artwork_Type_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:objectWorkTypeWrap/lido:objectWorkType',
    "Type_ID_Path": 'lido:conceptID[@lido:source]',
    #"Type_EntityType_Path": 'is a simple string named "type"',
    "Type_Label_Path": 'lido:term[not(@lido:addedSearchTerm)]',
    "Type_AltLabel_Path": 'lido:term[@lido:addedSearchTerm="yes"]',

    # LOCATION
    "Artwork_Location_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet',
    "Location_Label_Path": 'lido:repositoryName/lido:legalBodyName/lido:appellationValue',
    "Location_PlaceID_Path": 'lido:repositoryLocation/lido:placeID[@lido:source]',
    "Location_InventoryNumber_Path": 'lido:workId[@lido:type="Inventarnummer"]',
    "Location_PlaceLabel_Path": 'lido:repositoryLocation/lido:namePlaceSet/lido:appellationValue',##hat gleiche Name mit Location_Name_Path

    #GENRE
    "Artwork_Genre_Path": 'lido:descriptiveMetadata/lido:objectClassificationWrap/lido:classificationWrap/lido:classification',
    "Genre_ID_Path": 'lido:conceptID[@lido:source]',
    "Genre_Label_Path": 'lido:term',
    "Genre_AltLabel_Path": 'lido:term[@lido:addedSearchTerm="yes"]',
    "Genre_ClassificationType": '[@lido:type]',

    #ARTIST
    "Artwork_Artists_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventActor',
    "Artist_ID_Path": 'lido:actorInRole/lido:actor/lido:actorID[@lido:source]',
    "Artist_Name_Path": 'lido:actorInRole/lido:actor/lido:nameActorSet/lido:appellationValue[@lido:pref="preferred"]',
    "Artist_Altname_Path": 'lido:actorInRole/lido:actor/lido:nameActorSet/lido:appellationValue[@lido:pref="alternative"]',
    "Artist_Nationality_Path": 'lido:actorInRole/lido:actor/lido:nationalityActor/lido:term',
    "Artist_Birth_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:earliestDate[@lido:type="birthDate"]',
    "Artist_Death_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:latestDate[@lido:type="deathDate"]',
    "Artist_EvidenceFirst_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:earliestDate[@lido:type="evidenceDate"]',
    "Artist_EvidenceLast_Path": 'lido:actorInRole/lido:actor/lido:vitalDatesActor/lido:latestDate[@lido:type="evidenceDate"]',
    "Artist_Gender_Path": 'lido:actorInRole/lido:actor/lido:genderActor',
    "Artist_Roles_Path": 'lido:actorInRole/lido:roleActor/lido:term',

    #MATERIAL
    "Artwork_Materials_Path": 'lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventMaterialsTech',
    "Material_ID_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:conceptID[@lido:source]',
    "Material_name_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:term',
    "Material_AltLabel_Path": 'lido:materialsTech/lido:termMaterialsTech/lido:term[@lido:addedSearchTerm="yes"]',

    #ICONOGRAPHY
    "Artwork_Iconographies_Path": 'lido:descriptiveMetadata/lido:objectRelationWrap/lido:subjectWrap/lido:subjectSet/lido:subject[@lido:type="Beschreibung"]',
    "Iconography_Id_Path": 'lido:subjectConcept/lido:conceptID[@lido:source]',
    "Iconography_Label_Path": 'lido:subjectConcept/lido:term[@lido:pref="preferred"]',
    "Iconography_Alt_Label_Path": 'lido:subjectConcept/lido:term',
    "Iconography_Iconclass_Path": 'lido:subjectConcept/lido:term[last()]',

    #MEASUREMENT
    "Artwork_Measurements_Path": 'lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet',
    "Measurement_DisplayName_Path": 'lido:displayObjectMeasurements',
    "Measurement_Type_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementType',
    "Measurement_Unit_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementUnit',
    "Measurement_Value_Path": 'lido:objectMeasurements/lido:measurementsSet/lido:measurementValue',
    "Measurement_Extend_Path": 'lido:objectMeasurements/lido:extentMeasurements',
    "Measurement_Shape_Path": 'lido:objectMeasurements/lido:shapeMeasurements',
    "Measurement_Format_Path": 'lido:objectMeasurements/lido:formatMeasurements',
    "Measurement_Qualifier_Path": 'lido:objectMeasurements/lido:qualifierMeasurements',

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

}

