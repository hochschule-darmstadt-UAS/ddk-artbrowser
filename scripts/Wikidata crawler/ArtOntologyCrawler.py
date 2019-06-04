"""
Module to crawl artwork metadata from Wikidata and store them im *.csv files and a *.ttl file (RDF).
Can be executed in https://paws.wmflabs.org which provides Jupyter Notebooks for accessing Wikidata.
Requires being logged in at Wikimedia

Execute crawling using
extract_art_ontology()
This may take several hours.
"""



import pywikibot
import types
from pywikibot import pagegenerators as pg
import csv
import datetime
import ast



def extract_artworks(type_name, wikidata_id):
    """Extracts artworks metadata from Wikidata and stores them in a *.csv file.

    type_name -- e.g., 'drawings', will be used as filename
    wikidata_id -- e.g., 'wd:Q93184' Wikidata ID of a class; all instances of this class and all subclasses with label, creator, and image will be loaded.

    Examples:
    extract_artworks('drawings', 'wd:Q93184')
    extract_artworks('sculptures', 'wd:Q860861')
    extract_artworks('paintings', 'wd:Q3305213')
    """
    print(datetime.datetime.now(), "Starting with", type_name)
    QUERY = 'SELECT  ?item WHERE {SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } ?cls wdt:P279* ' + wikidata_id + ' . ?item wdt:P31 ?cls; wdt:P170 ?creator; wdt:P18 ?image .}'
    # all artworks of this type (including subtypes) with label, creator, and image
    wikidata_site = pywikibot.Site("wikidata", "wikidata")
    items = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)
    count = 0

    with open(type_name + ".csv", "w", newline="", encoding='utf-8') as file:
        fields = ["id", "classes", "label", "description", "image", "creators", "locations", "genres", "movements", "inception", "materials", "depicts", "country", "height",
                  "width"]
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';', quotechar='"')
        writer.writeheader()

        for item in items:
            #            if count > 50:
            #                continue

            # mandatory fields
            try:
                item_dict = item.get()
                label = item_dict["labels"]["en"]
                clm_dict = item_dict["claims"]
                classes = list(map(lambda clm: clm.getTarget().id, clm_dict["P31"]))
                image = clm_dict["P18"][0].getTarget().get_file_url()
                creators = list(map(lambda clm: clm.getTarget().id, clm_dict["P170"]))
            except:
                continue
                # optional fields
            try:
                description = item_dict["descriptions"]["en"]
            except:
                description = ""
            try:
                locations = list(map(lambda clm: clm.getTarget().id, clm_dict["P276"]))
            except:
                locations = []
            try:
                genres = list(map(lambda clm: clm.getTarget().id, clm_dict["P136"]))
            except:
                genres = []
            try:
                movements = list(map(lambda clm: clm.getTarget().id, clm_dict["P135"]))
            except:
                movements = []
            try:
                inception = clm_dict["P571"][0].getTarget().year
            except:
                inception = ""
            try:
                materials = list(map(lambda clm: clm.getTarget().id, clm_dict["P186"]))
            except:
                materials = []
            try:
                depicts = list(map(lambda clm: clm.getTarget().id, clm_dict["P180"]))
            except:
                depicts = []
            try:
                country = clm_dict["P17"][0].getTarget().get()["labels"]["en"]
            except:
                country = ""
            try:
                height = str(clm_dict["P2048"][0].getTarget().amount)
            except:
                height = ""
            try:
                width = str(clm_dict["P2049"][0].getTarget().amount)
            except:
                width = ""
            count += 1
            print(str(count) + " ", end='')
            writer.writerow(
                {"id": item.id, "classes": classes, "label": label, "description": description, "image": image, "creators": creators, "locations": locations, "genres": genres,
                 "movements": movements, "inception": inception, "materials": materials, "depicts": depicts, "country": country, "height": height, "width": width})
            # print(classes, item, label, description, image, creators, locations, genres, movements,  inception, materials, depicts,  country, height, width)

    print(datetime.datetime.now(), "Finished with", type_name)




def extract_subjects(subject_type):
    """Extracts metadata from Wikidata of a certain subject type and stores them in a *.csv file

    subject_type -- one of 'genres', 'movements', 'materials', 'depicts', 'creators', 'locations'. Will be used as filename

    Precondition: Files 'paintings.csv', 'drawings.csv', 'sculptures.csv' must have been created before (function extract_artworks).
    Metadata for artworks in theses files will be stored.

    Examples:
    extract_subjects('genres')
    extract_subjects('movements')
    extract_subjects('materials')
    extract_subjects('depicts')
    extract_subjects('creators')
    extract_subjects('locations')
    """
    print(datetime.datetime.now(), "Starting with", subject_type)
    subjects = set()
    file_names = ['paintings.csv', 'drawings.csv', 'sculptures.csv']
    for file_name in file_names:
        with open(file_name, newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';', quotechar='"')
            for row in reader:
                item_subjects = ast.literal_eval(row[subject_type])  # parses list from string
                for subject in item_subjects:
                    subjects.add(subject)

    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    print("Total: ", len(subjects), subject_type)
    count = 0
    with open(subject_type + ".csv", "w", newline="", encoding='utf-8') as file:
        fields = ["id", "classes", "label", "description", "image"]
        if subject_type == "creators":
            fields += ["gender", "date_of_birth", "date_of_death", "place_of_birth", "place_of_death", "citizenship", "movements", "influenced_by"]
        if subject_type == "movements":
            fields += ["influenced_by"]
        if subject_type == "locations":
            fields += ["country", "website", "part_of", "lat", "lon"]
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';', quotechar='"')
        writer.writeheader()

        for subject in subjects:
            #            if count > 50:
            #                continue
            try:
                item = pywikibot.ItemPage(repo, subject)
                item_dict = item.get()
                clm_dict = item_dict["claims"]
            except:
                continue
            try:
                classes = list(map(lambda clm: clm.getTarget().id, clm_dict["P31"]))
            except:
                classes = []
            try:
                label = item_dict["labels"]["en"]
            except:
                label = ""
            try:
                description = item_dict["descriptions"]["en"]
            except:
                description = ""
            try:
                image = clm_dict["P18"][0].getTarget().get_file_url()
            except:
                image = ""

            if subject_type == "creators":
                try:
                    gender = clm_dict["P21"][0].getTarget().get()["labels"]["en"]
                except:
                    gender = ""
                try:
                    date_of_birth = clm_dict["P569"][0].getTarget().year
                except:
                    date_of_birth = ""
                try:
                    date_of_death = clm_dict["P570"][0].getTarget().year
                except:
                    date_of_death = ""
                try:
                    place_of_birth = clm_dict["P19"][0].getTarget().get()["labels"]["en"]
                except:
                    place_of_birth = ""
                try:
                    place_of_death = clm_dict["P20"][0].getTarget().get()["labels"]["en"]
                except:
                    place_of_death = ""
                try:
                    citizenship = clm_dict["P27"][0].getTarget().get()["labels"]["en"]
                except:
                    citizenship = ""
                try:
                    movements = list(map(lambda clm: clm.getTarget().id, clm_dict["P135"]))
                except:
                    movements = []
                try:
                    influenced_by = list(map(lambda clm: clm.getTarget().id, clm_dict["P737"]))
                except:
                    influenced_by = []

            if subject_type == "movements":
                try:
                    influenced_by = list(map(lambda clm: clm.getTarget().id, clm_dict["P737"]))
                except:
                    influenced_by = []

            if subject_type == "locations":
                try:
                    country = clm_dict["P17"][0].getTarget().get()["labels"]["en"]
                except:
                    country = ""
                try:
                    website = clm_dict["P856"][0].getTarget()
                except:
                    website = ""
                try:
                    part_of = list(map(lambda clm: clm.getTarget().id, clm_dict["P361"]))
                except:
                    part_of = []
                try:
                    coordinate = clm_dict["P625"][0].getTarget()
                    lat = coordinate.lat
                    lon = coordinate.lon
                except:
                    lat = ""
                    lon = ""

            count += 1
            print(str(count) + " ", end='')
            if subject_type == "creators":
                writer.writerow({"id": item.id, "classes": classes, "label": label, "description": description, "image": image, "gender": gender, "date_of_birth": date_of_birth,
                                 "date_of_death": date_of_death, "place_of_birth": place_of_birth, "place_of_death": place_of_death, "citizenship": citizenship,
                                 "movements": movements, "influenced_by": influenced_by})
            if subject_type == "movements":
                writer.writerow({"id": item.id, "classes": classes, "label": label, "description": description, "image": image, "influenced_by": influenced_by})
            elif subject_type == "locations":
                writer.writerow(
                    {"id": item.id, "classes": classes, "label": label, "description": description, "image": image, "country": country, "website": website, "part_of": part_of,
                     "lat": lat, "lon": lon})
            else:
                writer.writerow({"id": item.id, "classes": classes, "label": label, "description": description, "image": image})

    print()
    print(datetime.datetime.now(), "Finished with", subject_type)




def extract_classes():
    """Extracts metadata of classes from Wikidata and stores them in a *.csv file


    Precondition: Files 'paintings.csv', 'drawings.csv', 'sculptures.csv', 'genres.csv', 'movements.csv', 'materials.csv', 'depicts.csv', 'creators.csv', 'locations.csv' must have been created before (functions extract_artworks and extract_subjects).
    Metadata for classes referenced in theses files will be stored.
    """
    print(datetime.datetime.now(), "Starting with classes")
    classes = set()
    class_dict = dict()
    file_names = ['paintings.csv', 'drawings.csv', 'sculptures.csv', 'genres.csv', 'movements.csv', 'materials.csv', 'depicts.csv', 'creators.csv', 'locations.csv']

    for file_name in file_names:
        with open(file_name, newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';', quotechar='"')
            for row in reader:
                item_classes = ast.literal_eval(row['classes'])  # parses list from string
                for item_class in item_classes:
                    classes.add(item_class)

    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    print("Total: ", len(classes), "classes")
    count = 0

    for cls in classes:
        #        if count > 10:
        #            continue
        extract_class(cls, class_dict, repo)
        count += 1
        print(str(count) + " ", end='')
    with open("classes.csv", "w", newline="", encoding='utf-8') as file:
        fields = ["id", "label", "description", "subclass_of"]
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';', quotechar='"')
        writer.writeheader()
        for cls in class_dict:
            writer.writerow(class_dict[cls])

    print()
    print(datetime.datetime.now(), "Finished with classes")


def extract_class(cls, class_dict, repo):
    """Extracts metadata of a class and it superclasses from Wikidata and stores them in a dictionary

    cls -- ID of a Wikidata class
    class_dict -- dictionary with Wikidata ID as key and a dict of class attributes as value; will be updated
    repo -- Wikidata repository as accessed using pywikibot
    """
    if not cls in class_dict:
        try:
            item = pywikibot.ItemPage(repo, cls)
            item_dict = item.get()
            clm_dict = item_dict["claims"]
        except:
            print("except " + str(cls))
            return
        try:
            label = item_dict["labels"]["en"]
        except:
            label = ""
        try:
            description = item_dict["descriptions"]["en"]
        except:
            description = ""
        try:
            subclass_of = list(map(lambda clm: clm.getTarget().id, clm_dict["P279"]))
        except:
            subclass_of = []
        class_dict[cls] = {"id": item.id, "label": label, "description": description, "subclass_of": subclass_of}
        for superclass in subclass_of:
            extract_class(superclass, class_dict, repo)




def merge_artworks():
    """Merges artworks from files 'paintings.csv', 'drawings.csv', 'sculptures.csv' (function extract_artworks) and stores them in a new file artworks.csv
    """
    print(datetime.datetime.now(), "Starting with", "merging artworks")
    artworks = set()
    file_names = ['paintings.csv', 'drawings.csv', 'sculptures.csv']

    with open("artworks.csv", "w", newline="", encoding='utf-8') as output:
        fields = ["id", "classes", "label", "description", "image", "creators", "locations", "genres", "movements", "inception", "materials", "depicts", "country", "height",
                  "width"]
        writer = csv.DictWriter(output, fieldnames=fields, delimiter=';', quotechar='"')
        writer.writeheader()
        for file_name in file_names:
            with open(file_name, newline="", encoding='utf-8') as input:
                reader = csv.DictReader(input, delimiter=';', quotechar='"')
                for row in reader:
                    if not row['id'] in artworks:  # remove duplicates
                        writer.writerow(row)
                        artworks.add(row['id'])

    print()
    print(datetime.datetime.now(), "Finished with", "merging artworks")




def generate_rdf():
    """Generates an RDF Tutle file 'ArtOntology.ttl' from *.csv files generated by functions extract_artworks, extract_subjects, extract_classes and merge_artworks"""
    print(datetime.datetime.now(), "Starting with", "generating rdf")

    configs = {
        'classes': {'filename': 'classes.csv', 'class': 'rdfs:Class'},
        'movements': {'filename': 'movements.csv', 'class': ':movement'},
        'movements': {'filename': 'movements.csv', 'class': ':movement'},
        'genre': {'filename': 'genres.csv', 'class': ':genre'},
        'materials': {'filename': 'materials.csv', 'class': ':material'},
        'locations': {'filename': 'locations.csv', 'class': ':location'},
        'materials': {'filename': 'materials.csv', 'class': ':material'},
        'objects': {'filename': 'depicts.csv', 'class': ':object'},
        'persons': {'filename': 'creators.csv', 'class': ':person'},
        'artworks': {'filename': 'artworks.csv', 'class': ':artwork'}
    }
    properties = {
        'label': {'property': 'rdfs:label', 'type': 'string'},
        'description': {'property': ':description', 'type': 'string'},
        'image': {'property': ':image', 'type': 'url'},
        'creators': {'property': ':creator', 'type': 'list'},
        'locations': {'property': ':location', 'type': 'list'},
        'genres': {'property': ':genre', 'type': 'list'},
        'movements': {'property': ':movement', 'type': 'list'},
        'inception': {'property': ':inception', 'type': 'number'},
        'materials': {'property': ':material', 'type': 'list'},
        'depicts': {'property': ':depicts', 'type': 'list'},
        'country': {'property': ':country', 'type': 'string'},
        'height': {'property': ':height', 'type': 'number'},
        'width': {'property': ':width', 'type': 'number'},
        'gender': {'property': ':gender', 'type': 'string'},
        'date_of_birth': {'property': ':date_of_birth', 'type': 'number'},
        'date_of_death': {'property': ':date_of_death', 'type': 'number'},
        'place_of_birth': {'property': ':place_of_birth', 'type': 'string'},
        'place_of_death': {'property': ':place_of_death', 'type': 'string'},
        'influenced_by': {'property': ':influenced_by', 'type': 'list'},
        'website': {'property': ':website', 'type': 'url'},
        'part_of': {'property': ':part_of', 'type': 'list'},
        'lat': {'property': ':lat', 'type': 'number'},
        'lon': {'property': ':lon', 'type': 'number'},
        'subclass_of': {'property': 'rdfs:subClassOf', 'type': 'list'}
    }
    quotechars = {
        'string': {'start': '"', 'end': '"'},
        'url': {'start': '<', 'end': '>'},
        'number': {'start': '', 'end': ''}
    }

    with open("ArtOntology.ttl", "w", newline="", encoding='utf-8') as output:
        with open('ArtOntologyHeader.txt', newline="", encoding='utf-8') as input:
            output.write(input.read())  # copy header

        for config in configs:
            print(config)
            output.write('\n\n\n# ' + config + '\n\n')
            with open(configs[config]['filename'], newline="", encoding='utf-8') as input:
                # count = 0
                reader = csv.DictReader(input, delimiter=';', quotechar='"')
                for row in reader:
                    # if count > 10:
                    # continue
                    # else:
                    # count +=1
                    output.write('wd:' + row['id'] + ' rdf:type ' + configs[config]['class'])
                    if 'classes' in row:  # classes.csv has no classes column
                        classes = ast.literal_eval(row['classes'])  # parses list of class names from string
                        for cls in classes:
                            output.write(', wd:' + cls)
                    for entry in row:
                        if entry in properties:
                            tpe = properties[entry]['type']
                            if tpe in quotechars.keys():
                                value = row[entry]
                                if value != '':  # cell not empty
                                    if tpe == 'string' and '"' in value:
                                        value = value.replace('"', "'")  # replace double quotes by single quotes
                                    output.write(' ;\n    ' + properties[entry]['property'] + ' ' + quotechars[tpe]['start'] + value + quotechars[tpe]['end'])
                            elif tpe == 'list':
                                if row[entry] != '':  # cell not empty - should not happen
                                    ids = ast.literal_eval(row[entry])  # parses list of ids from string
                                    if len(ids) > 0:
                                        first = True
                                        output.write(' ;\n    ' + properties[entry]['property'] + ' ')
                                        for id in ids:
                                            if first:
                                                first = False
                                            else:
                                                output.write(' , ')
                                            output.write('wd:' + id)
                            else:
                                raise Exception('Unexpected type: ' + tpe)
                    output.write(' .\n')

    print()
    print(datetime.datetime.now(), "Finished with", "generating rdf")




def extract_art_ontology():
    """Extracts *.csv files and a *.ttl file with metadata for artworks from Wikidata"""

    extract_artworks("drawings", "wd:Q93184")
    extract_artworks("sculptures", "wd:Q860861")
    extract_artworks("paintings", "wd:Q3305213")

    extract_subjects("genres")
    extract_subjects("movements")
    extract_subjects("materials")
    extract_subjects("depicts")
    extract_subjects("creators")
    extract_subjects("locations")
    extract_classes()

    merge_artworks()

    generate_rdf()


