import csv
import datetime
import hashlib
import inspect
import json
import logging
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError

from pywikibot import WbTime
from SPARQLWrapper import JSON, SPARQLWrapper

import utils.open_art_browser_constants as constant
import utils.request_utils as request_utils
import utils.util_funcs as util_funcs

logging.basicConfig(
    filename="get_wikidata_items.log", filemode="w", level=logging.DEBUG
)

DEV = True
DEV_CHUNK_LIMIT = 2  # Not entry but chunks of 50

# All properties extracted from the wikidata entities mapped to their openartbrowser key-label
property_name_to_property_id = {
    "image": "P18",
    "class": "P31",  # Is called "instance of" in wikidata
    "artist": "P170",  # Is called "creator" in wikidata
    "location": "P276",
    "start_time": "P580",
    "end_time": "P582",
    "genre": "P136",
    "movement": "P135",
    "inception": "P571",
    "material": "P186",  # Is called "material used" in wikidata
    "motif": "P180",  # Is called "depicts" in wikidata
    "country": "P17",
    "height": "P2048",
    "width": "P2049",
    "length": "P2043",
    "diameter": "P2386",
    "unit_symbol": "P5061",
    "iconclass": "P1257",
    "main_subject": "P921",
    "influenced_by": "P737",
    "gender": "P21",  # Is called "sex or gender" in wikidata
    "date_of_birth": "P569",
    "date_of_death": "P570",
    "place_of_birth": "P19",
    "place_of_death": "P20",
    "citizenship": "P27",  # Is called "country of citizenship" in wikidata
    "website": "P856",  # Is called "official website" in wikidata
    "part_of": "P361",
    "has_part": "P527",
    "coordinate": "P625",  # Is called "coordinate location" in wikidata
    "subclass_of": "P279",
}


def query_artwork_qids(type_name, wikidata_id):
    """ Extracts all artwork QIDs from the wikidata SPARQL endpoint https://query.wikidata.org/ """
    artwork_ids_filepath = Path(__file__).parent.absolute() / "artwork_ids_query.sparql"
    QID_BY_ARTWORK_TYPE_QUERY = (
        open(artwork_ids_filepath, "r", encoding="utf8")
        .read()
        .replace("$QID", wikidata_id)
    )

    sparql = SPARQLWrapper(
        "https://query.wikidata.org/sparql", agent=util_funcs.agent_header()
    )

    wikidata_entity_url = "http://www.wikidata.org/entity/"

    sparql.setQuery(QID_BY_ARTWORK_TYPE_QUERY)
    sparql.setReturnFormat(JSON)

    # ToDo: refactor would be better without while True
    while True:
        try:
            query_result = sparql.query().convert()
            break
        except HTTPError as error:
            print(error)
            print("Waiting for 5 seconds")
            time.sleep(5)
            if error.errno != 403:
                continue
            else:
                print("Looks like the bot was blocked.")
                exit(-1)

    artwork_ids = list(
        map(
            lambda result: result["item"]["value"].replace(wikidata_entity_url, ""),
            query_result["results"]["bindings"],
        )
    )
    print(f"{type_name}: {len(artwork_ids)} ids from SPARQL query")

    return artwork_ids


def wikidata_entity_request(
    qids,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
    props=["claims", "descriptions", "labels", "sitelinks"],
    timeout=constant.TIMEOUT,
    sleep_time=constant.SLEEP_TIME,
    maxlag=constant.MAX_LAG,
):
    """ Represents one artwork request for n-items
        The API specifies that 50 items can be loaded at once without needing additional permissions:
        https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities
    """
    initial_timeout = timeout
    langkeyPlusWikiList = [key + "wiki" for key in languageKeys]
    parameters = {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "format": "json",
        "languages": "|".join(languageKeys),
        "sitefilter": "|".join(langkeyPlusWikiList),
        "props": "|".join(props),
        # if the server needs more than maxlag seconds to process
        # the query an error response is returned
        "maxlag": maxlag,
    }

    url = "https://www.wikidata.org/w/api.php"
    return request_utils.send_http_request(
        parameters,
        constant.HTTP_HEADER,
        url,
        logging,
        initial_timeout=initial_timeout,
        items=qids,
        timeout=timeout,
        sleep_time=sleep_time,
        maxlag=maxlag,
    )


def get_image_url_by_name(image_name) -> str:
    image_name = image_name.replace(" ", "_")
    hash = hashlib.md5(image_name.encode("utf-8")).hexdigest()
    hash_index_1 = hash[0]
    hash_index_1_and_2 = hash[0] + hash[1]
    url = "https://upload.wikimedia.org/wikipedia/commons/{0}/{1}/{2}".format(
        hash_index_1, hash_index_1_and_2, image_name
    )
    return url


def return_on_failure(return_value):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param return_value: The return value of func in case of an exception
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                error_message = "Error in function {0} on item {1}".format(
                    func.__name__, args[0]["id"]
                )
                # iterate over argument names
                for index, param in enumerate(inspect.getfullargspec(func)[0][1:], 1):
                    error_message += ", {0} {1}".format(param, args[index])
                error_message += ", error {0}".format(error)
                logging.info(error_message)

                return return_value

        return wrapper

    return decorator


@return_on_failure("")
def try_get_label_or_description(entity_dict, fieldname, langkey):
    """ Method to extract the label or description """
    return entity_dict[fieldname][langkey]["value"]


@return_on_failure("")
def try_get_wikipedia_link(entity_dict, langkey):
    return "https://{0}.wikipedia.org/wiki/{1}".format(
        langkey, entity_dict["sitelinks"][f"{langkey}wiki"]["title"].replace(" ", "_"),
    )


@return_on_failure("")
def try_get_dimension_value(entity_dict, property_id):
    return float(
        entity_dict["claims"][property_id][0]["mainsnak"]["datavalue"]["value"][
            "amount"
        ]
    )


@return_on_failure("")
def try_get_dimension_unit(entity_dict, property_id):
    unit_qid = entity_dict["claims"][property_id][0]["mainsnak"]["datavalue"]["value"][
        "unit"
    ].replace("http://www.wikidata.org/entity/", "")
    qid_pattern = r"^Q\d+"
    is_qid = re.match(qid_pattern, unit_qid)
    if is_qid:
        return unit_qid
    else:
        logging.error(
            "Error on item {0}, property {1}, Unit was provided but isn't a QID reference".format(
                entity_dict["id"], property_id
            )
        )
        return ""


@return_on_failure([])
def try_get_qid_reference_list(entity_dict, property_id):
    """ Method to extract the references (which are qids) as a list """
    return list(
        map(
            lambda clm: clm["mainsnak"]["datavalue"]["value"]["id"],
            entity_dict["claims"][property_id],
        )
    )


@return_on_failure("")
def try_get_first_value(entity_dict, property_id):
    return entity_dict["claims"][property_id][0]["mainsnak"]["datavalue"]["value"]


@return_on_failure([])
def try_get_value_list(entity_dict, property_id):
    """ Method to extract iconclasses """
    return list(
        map(
            lambda clm: clm["mainsnak"]["datavalue"]["value"],
            entity_dict["claims"][property_id],
        )
    )


@return_on_failure("")
def try_get_year_from_property_timestamp(entity_dict, property_id):
    """ Method to extract the year from an inception timestamp """
    timestr = entity_dict["claims"][property_id][0]["mainsnak"]["datavalue"]["value"][
        "time"
    ]
    return WbTime.fromTimestr(timestr).year


@return_on_failure("")
def try_get_first_qid(entity_dict, property_id):
    """ Method to extract the first qid """
    return entity_dict["claims"][property_id][0]["mainsnak"]["datavalue"]["value"]["id"]


@return_on_failure("no unit")
def try_get_unit_symbol(entity_dict, property_id):
    unit_symbol_entries = entity_dict["claims"][property_id]
    for unit_symbol_entry in unit_symbol_entries:
        if unit_symbol_entry["mainsnak"]["datavalue"]["value"]["language"] == "en":
            return unit_symbol_entry["mainsnak"]["datavalue"]["value"]["text"]


def extract_artworks(
    type_name,
    wikidata_id,
    already_crawled_wikidata_items,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    """Extracts artworks metadata from Wikidata and stores them in a dictionary.

    type_name -- e.g., 'drawings', will be used as filename
    wikidata_id -- e.g., 'wd:Q93184' Wikidata ID of a class; all instances of this class and all subclasses with label, artist, and image will be loaded.
    languageKeys -- e.g, list('en', 'de')

    Examples:
    extract_artworks('drawings', 'wd:Q93184', '('en', 'de'))
    extract_artworks('sculptures', 'wd:Q860861', '('en', 'de'))
    extract_artworks('paintings', 'wd:Q3305213', '('en', 'de'))
    """
    print(datetime.datetime.now(), "Starting with", type_name)

    extract_dicts = []
    chunk_count = 0
    item_count = 0
    artwork_ids = query_artwork_qids(type_name, wikidata_id)

    # Don't load items again, if they were loaded in another artwork category
    for artwork_id in artwork_ids:
        if artwork_id in already_crawled_wikidata_items:
            artwork_ids.remove(artwork_id)

    print(
        f"{len(artwork_ids)} {type_name} entries are not loaded yet, starting now. Already crawled item count is {len(already_crawled_wikidata_items)}"
    )
    chunk_size = 50  # The chunksize 50 is allowed by the wikidata api, bigger numbers need special permissions
    artwork_id_chunks = util_funcs.chunks(artwork_ids, chunk_size)
    for chunk in artwork_id_chunks:
        if DEV and chunk_count == DEV_CHUNK_LIMIT:
            logging.debug(
                f"DEV_CHUNK_LIMIT of {type_name} reached. End extraction for {type_name}"
            )
            break

        query_result = wikidata_entity_request(chunk)
        if "entities" not in query_result:
            logging.warn("Skipping chunk")
            continue

        for result in query_result["entities"].values():
            try:
                qid = result["id"]
                # How to get image url
                # https://stackoverflow.com/questions/34393884/how-to-get-image-url-property-from-wikidata-item-by-api
                image = get_image_url_by_name(
                    result["claims"][property_name_to_property_id["image"]][0][
                        "mainsnak"
                    ]["datavalue"]["value"]
                )
            except Exception as error:
                logging.warning(
                    "Error on qid or image, skipping item. Error: {0}".format(error)
                )
                continue

            label = try_get_label_or_description(result, "labels", "en")
            description = try_get_label_or_description(result, "descriptions", "en")

            (
                classes,
                artists,
                locations,
                genres,
                movements,
                materials,
                motifs,
                main_subjects,
            ) = get_attribute_values_with_try_get_func(
                result,
                [
                    "class",
                    "artist",
                    "location",
                    "genre",
                    "movement",
                    "material",
                    "motif",
                    "main_subject",
                ],
                try_get_qid_reference_list,
            )

            iconclasses = try_get_value_list(
                result, property_name_to_property_id["iconclass"]
            )
            inception = try_get_year_from_property_timestamp(
                result, property_name_to_property_id["inception"]
            )
            country = try_get_first_qid(result, property_name_to_property_id["country"])

            # Resolve dimensions
            # The units are qids which have to be resolved later
            height, width, length, diameter = get_attribute_values_with_try_get_func(
                result,
                ["height", "width", "length", "diameter"],
                try_get_dimension_value,
            )
            (
                height_unit,
                width_unit,
                length_unit,
                diameter_unit,
            ) = get_attribute_values_with_try_get_func(
                result,
                ["height", "width", "length", "diameter"],
                try_get_dimension_unit,
            )

            artwork_dictionary = {
                "id": qid,
                "classes": classes,
                "label": label,
                "description": description,
                "image": image,
                "artists": artists,
                "locations": locations,
                "genres": genres,
                "movements": movements,
                "inception": inception,
                "materials": materials,
                "motifs": motifs,
                "country": country,
                "height": height,
                "height_unit": height_unit,
                "width": width,
                "width_unit": width_unit,
                "length": length,
                "length_unit": length_unit,
                "diameter": diameter,
                "diameter_unit": diameter_unit,
                "iconclasses": iconclasses,
                "main_subjects": main_subjects,
            }

            for langkey in languageKeys:
                label_lang = try_get_label_or_description(result, "labels", langkey)
                description_lang = try_get_label_or_description(
                    result, "descriptions", langkey
                )
                wikipedia_link_lang = try_get_wikipedia_link(result, langkey)
                artwork_dictionary.update(
                    {
                        "label_" + langkey: label_lang,
                        "description_" + langkey: description_lang,
                        "wikipediaLink_" + langkey: wikipedia_link_lang,
                    }
                )
            extract_dicts.append(artwork_dictionary)
            already_crawled_wikidata_items.add(qid)

        item_count += len(chunk)
        print(f"Status of {type_name}: {item_count}/{len(artwork_ids)}")

        chunk_count += 1

    print(datetime.datetime.now(), "Finished with", type_name)
    return extract_dicts


def get_attribute_values_with_try_get_func(result, item_list, try_get_func):
    for item in item_list:
        yield try_get_func(result, property_name_to_property_id[item])


def extract_art_ontology():
    """ Extracts *.csv and *.JSON files for artworks from Wikidata """

    # Array of already crawled wikidata items
    already_crawled_wikidata_items = set()

    for artwork, wd in [
        ("drawings", "wd:Q93184"),
        ("sculptures", "wd:Q860861"),
        ("paintings", "wd:Q3305213"),
    ]:
        extracted_artwork = extract_artworks(
            artwork, wd, already_crawled_wikidata_items
        )

        path_name = create_new_path("artworks", artwork, "csv")
        generate_csv(artwork, extracted_artwork, get_fields(artwork), path_name)

        path_name = create_new_path("artworks", artwork, "json")
        generate_json(artwork, extracted_artwork, path_name)

    merged_artworks = merge_artworks()

    path_name = create_new_path("artworks", file_type="csv")
    generate_csv(
        "artworks", merged_artworks, get_fields("artworks") + ["type"], path_name
    )

    # Get motifs and main subjects
    motifs = extract_motifs_and_main_subjects(merged_artworks)

    # Get extracted genres, materials, etc.
    genres, materials, movements, artists, locations = bundle_extract_data_calls(
        ["genres", "materials", "movements", "artists", "locations"], merged_artworks
    )

    # Get distinct classes from artworks, motifs, etc.
    extracted_classes = get_distinct_extracted_classes(
        merged_artworks, motifs, genres, materials, movements, artists, locations,
    )

    # Get country labels for merged artworks and locations
    (
        locations,
        merged_artworks,
        movements,
    ) = get_country_labels_for_merged_artworks_and_locations(
        locations, merged_artworks, movements
    )

    # Get labels for artists
    artists = get_labels_for_artists(
        artists, ["gender", "place_of_birth", "place_of_death", "citizenship"]
    )

    # Get unit symbols from qid for artworks
    distinct_unit_qids = get_unit_symbols_from_qid(merged_artworks)
    unit_symbols = get_unit_symbols(distinct_unit_qids)
    resolve_unit_id_to_unit_symbol(merged_artworks, unit_symbols)

    # Write to JSON
    write_data_to_json(
        motifs,
        genres,
        extracted_classes,
        materials,
        movements,
        locations,
        merged_artworks,
        artists,
    )


def extract_motifs_and_main_subjects(merged_artworks):
    motifs = get_distinct_attribute_values_from_dict("motifs", merged_artworks)
    main_subjects = get_distinct_attribute_values_from_dict(
        "main_subjects", merged_artworks
    )

    motifs_and_main_subjects = motifs | main_subjects
    motifs = get_subject("motifs and main subjects", motifs_and_main_subjects)
    return motifs


def write_data_to_json(
    motifs,
    genres,
    extracted_classes,
    materials,
    movements,
    locations,
    merged_artworks,
    artists,
):
    generate_json("motif", motifs, create_new_path("motifs"))
    generate_json("genre", genres, create_new_path("genres"))
    generate_json("class", extracted_classes, create_new_path("classes"))
    generate_json("material", materials, create_new_path("materials"))
    generate_json("movement", movements, create_new_path("movements"))
    generate_json("location", locations, create_new_path("locations"))
    generate_json("artwork", merged_artworks, create_new_path("artworks"))
    generate_json("artist", artists, create_new_path("artists"))


def get_unit_symbols_from_qid(merged_artworks):
    distinct_unit_qids = get_distinct_attribute_values_from_dict(
        "height_unit", merged_artworks, True
    )

    for item in ["width_unit", "length_unit", "diameter_unit"]:
        distinct_unit_qids = distinct_unit_qids.union(
            get_distinct_attribute_values_from_dict(item, merged_artworks, True)
        )
    return distinct_unit_qids


def get_labels_for_artists(artists, prop_list):
    for item in prop_list:
        distinct_label = get_distinct_attribute_values_from_dict(item, artists, True)
        extracted_labels = get_entity_labels(item, distinct_label)
        resolve_entity_id_to_label(item, artists, extracted_labels)
    return artists


def get_distinct_extracted_classes(
    merged_artworks, motifs, genres, materials, movements, artists, locations
):
    distinct_classes = get_distinct_attribute_values_from_dict(
        "classes", merged_artworks
    )
    distinct_classes = bundle_class_union_calls(
        distinct_classes, [motifs, genres, materials, movements, artists, locations],
    )
    return get_classes("classes", distinct_classes)


def get_country_labels_for_merged_artworks_and_locations(
    locations, merged_artworks, movements
):
    tmp = [locations, merged_artworks, movements]
    distinct_ids = [
        get_distinct_attribute_values_from_dict("country", item, True) for item in tmp
    ]

    distinct_country_ids = distinct_ids[0].union(distinct_ids[1], distinct_ids[2])
    country_labels_extracted = get_entity_labels("country", distinct_country_ids)

    for item in tmp:
        yield resolve_entity_id_to_label("country", item, country_labels_extracted)


def bundle_class_union_calls(distinct_classes, data_list):
    for item in data_list:
        distinct_classes = distinct_classes | get_distinct_attribute_values_from_dict(
            "classes", item
        )
    return distinct_classes


def create_new_path(name, subpath="", file_type="json"):
    return (
        Path.cwd()
        / "crawler_output"
        / "intermediate_files"
        / file_type
        / name
        / subpath
    )


def bundle_extract_data_calls(name_list, merged_artworks):
    for item in name_list:
        tmp = get_distinct_attribute_values_from_dict(item, merged_artworks)
        yield get_subject(item, tmp)


def get_fields(
    type_name, languageKeys=[item[0] for item in util_funcs.language_config_to_list()]
):
    """ Returns all fields / columns for a specific type, e. g. 'artworks' """
    fields = ["id", "classes", "label", "description", "image"]
    for langkey in languageKeys:
        fields += [
            "label_" + langkey,
            "description_" + langkey,
            "wikipediaLink_" + langkey,
        ]
    if type_name in ["drawings", "sculptures", "paintings", "artworks"]:
        fields += [
            "artists",
            "locations",
            "genres",
            "movements",
            "inception",
            "materials",
            "motifs",
            "country",
            "height",
            "height_unit",
            "width",
            "width_unit",
            "diameter",
            "diameter_unit",
            "length",
            "length_unit",
            "iconclasses",
            "main_subjects",
        ]
        for langkey in languageKeys:
            fields += ["country_" + langkey]
    elif type_name == "artists":
        fields += [
            "gender",
            "date_of_birth",
            "date_of_death",
            "place_of_birth",
            "place_of_death",
            "citizenship",
            "movements",
            "influenced_by",
        ]
        for langkey in languageKeys:
            fields += ["gender_" + langkey, "citizenship_" + langkey]
    elif type_name == "movements":
        fields += ["influenced_by"]
    elif type_name == "locations":
        fields += ["country", "website", "part_of", "lat", "lon"]
        for langkey in languageKeys:
            fields += ["country_" + langkey]
    elif type_name == "classes":
        fields = ["id", "label", "description", "subclass_of"]
        for langkey in languageKeys:
            fields += ["label_" + langkey, "description_" + langkey]
    return fields


def generate_csv(name, extract_dicts, fields, filename):
    """ Generates a csv file from a dictionary """
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename.with_suffix(".csv"), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=";", quotechar='"')
        writer.writeheader()
        for extract_dict in extract_dicts:
            writer.writerow(extract_dict)


def generate_json(name, extract_dicts, filename):
    """ Generates a JSON file from a dictionary """
    if len(extract_dicts) == 0:
        return
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename.with_suffix(".json"), "w", newline="", encoding="utf-8") as file:
        arrayToDump = []
        for extract_dict in extract_dicts:
            extract_dict["type"] = name
            arrayToDump.append(extract_dict)
        file.write(json.dumps(arrayToDump, ensure_ascii=False))


def merge_artworks():
    """ Merges artworks from files 'paintings.json', 'drawings.json',
        'sculptures.json' (function extract_artworks) and
        stores them in a dictionary.
    """
    print(datetime.datetime.now(), "Starting with", "merging artworks")
    artworks = set()
    file_names = ["paintings.json", "drawings.json", "sculptures.json"]
    file_names = [
        create_new_path("artworks", subpath=file_name) for file_name in file_names
    ]
    extract_dicts = []

    for file_name in file_names:
        with open(file_name, encoding="utf-8") as input:
            object_array = json.load(input)
            for object in object_array:
                if not object["id"] in artworks:  # remove duplicates
                    object["type"] = "artwork"
                    extract_dicts.append(object)
                    artworks.add(object["id"])

    print(datetime.datetime.now(), "Finished with", "merging artworks")
    print()
    return extract_dicts


def get_distinct_attribute_values_from_dict(
    attribute_name, entry_dict, is_single_value_column=False
):
    attribute_set = set()
    for json_object in entry_dict:
        if is_single_value_column:
            value = json_object[attribute_name]
            if value != "":
                attribute_set.add(value)
        else:
            for values in json_object[attribute_name]:
                attribute_set.add(values)

    return attribute_set


def try_map_response_to_subject(
    response,
    type_name,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    """
    Maps the default attributes which every subject has:
    qid, image, label, description, classes, wikipediaLink (including language specific attributes)
    """
    try:
        qid = response["id"]
    except Exception as error:
        logging.warning("Error on qid, skipping item. Error: {0}".format(error))
        return None

    # ToDo: Extract to function
    # How to get image url
    # https://stackoverflow.com/questions/34393884/how-to-get-image-url-property-from-wikidata-item-by-api
    try:
        image = get_image_url_by_name(
            response["claims"][property_name_to_property_id["image"]][0]["mainsnak"][
                "datavalue"
            ]["value"]
        )
    except:
        image = ""
    label = try_get_label_or_description(response, "labels", "en")
    description = try_get_label_or_description(response, "descriptions", "en")
    classes = try_get_qid_reference_list(
        response, property_name_to_property_id["class"]
    )

    subject_dict = {
        "id": qid,
        "classes": classes,
        "label": label,
        "description": description,
        "image": image,
    }

    for langkey in languageKeys:
        label_lang = try_get_label_or_description(response, "labels", langkey)
        description_lang = try_get_label_or_description(
            response, "descriptions", langkey
        )
        wikipedia_link_lang = try_get_wikipedia_link(response, langkey)
        subject_dict.update(
            {
                "label_" + langkey: label_lang,
                "description_" + langkey: description_lang,
                "wikipediaLink_" + langkey: wikipedia_link_lang,
            }
        )

    return subject_dict


def try_map_response_to_artist(response):
    gender = try_get_first_qid(response, property_name_to_property_id["gender"])
    date_of_birth = try_get_year_from_property_timestamp(
        response, property_name_to_property_id["date_of_birth"]
    )
    date_of_death = try_get_year_from_property_timestamp(
        response, property_name_to_property_id["date_of_death"]
    )
    # labels to be resolved later
    place_of_birth = try_get_first_qid(
        response, property_name_to_property_id["place_of_birth"]
    )
    # labels to be resolved later
    place_of_death = try_get_first_qid(
        response, property_name_to_property_id["place_of_death"]
    )
    # labels to be resolved later
    citizenship = try_get_first_qid(
        response, property_name_to_property_id["citizenship"]
    )
    movements = try_get_qid_reference_list(
        response, property_name_to_property_id["movement"]
    )
    return {
        "gender": gender,
        "date_of_birth": date_of_birth,
        "date_of_death": date_of_death,
        "place_of_birth": place_of_birth,
        "place_of_death": place_of_death,
        "citizenship": citizenship,
        "movements": movements,
    }


def try_map_response_to_movement(response):
    start_time = try_get_year_from_property_timestamp(
        response, property_name_to_property_id["start_time"]
    )
    end_time = try_get_year_from_property_timestamp(
        response, property_name_to_property_id["end_time"]
    )
    # labels to be resolved later
    country = try_get_first_qid(response, property_name_to_property_id["country"])
    has_part = try_get_qid_reference_list(
        response, property_name_to_property_id["has_part"]
    )
    part_of = try_get_qid_reference_list(
        response, property_name_to_property_id["part_of"]
    )
    return {
        "start_time": start_time,
        "end_time": end_time,
        "country": country,
        "has_part": has_part,
        "part_of": part_of,
    }


def try_map_response_to_location(response):
    country = try_get_first_qid(response, property_name_to_property_id["country"])
    website = try_get_first_value(response, property_name_to_property_id["website"])
    part_of = try_get_qid_reference_list(
        response, property_name_to_property_id["part_of"]
    )
    try:
        coordinate = response["claims"][property_name_to_property_id["coordinate"]][0][
            "mainsnak"
        ]["datavalue"]["value"]
        lat = coordinate["latitude"]
        lon = coordinate["longitude"]
    except Exception as error:
        logging.info(
            "Error on item {0}, property {1}, error {2}".format(
                response["id"], property_name_to_property_id["coordinate"], error
            )
        )
        lat = ""
        lon = ""
    return {
        "country": country,
        "website": website,
        "part_of": part_of,
        "lat": lat,
        "lon": lon,
    }


def get_subject(
    type_name,
    qids,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    print(datetime.datetime.now(), f"Starting with {type_name}")
    print(f"Total {type_name} to extract: {len(qids)}")
    item_count = 0
    extract_dicts = []
    chunk_size = 50  # The chunksize 50 is allowed by the wikidata api, bigger numbers need special permissions
    subject_id_chunks = util_funcs.chunks(list(qids), chunk_size)
    for chunk in subject_id_chunks:
        query_result = wikidata_entity_request(chunk)

        if "entities" not in query_result:
            logging.warn("Skipping chunk")
            continue

        for result in query_result["entities"].values():
            subject_dict = try_map_response_to_subject(result, type_name)
            if subject_dict is None:
                continue
            if type_name == "movements" or type_name == "artists":
                influenced_by = try_get_qid_reference_list(
                    result, property_name_to_property_id["influenced_by"]
                )
                subject_dict.update({"influenced_by": influenced_by})
            if type_name == "movements":
                subject_dict.update(try_map_response_to_movement(result))
            if type_name == "artists":
                subject_dict.update(try_map_response_to_artist(result))
            if type_name == "locations":
                subject_dict.update(try_map_response_to_location(result))
            extract_dicts.append(subject_dict)

        item_count += len(chunk)
        print(f"Status of {type_name}: {item_count}/{len(qids)}")

    print(datetime.datetime.now(), f"Finished with {type_name}")
    return extract_dicts


def get_entity_labels(
    type_name,
    qids,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    print(datetime.datetime.now(), f"Starting with {type_name} labels")
    print(f"Total {type_name} labels to extract: {len(qids)}")
    item_count = 0
    extract_dicts = []
    chunk_size = 50  # The chunksize 50 is allowed by the wikidata api, bigger numbers need special permissions
    id_chunks = util_funcs.chunks(list(qids), chunk_size)
    for chunk in id_chunks:
        query_result = wikidata_entity_request(
            chunk, props=["labels"], timeout=10
        )  # country entities take longer so timeout is increased

        if "entities" not in query_result:
            logging.warn("Skipping chunk")
            continue

        for result in query_result["entities"].values():
            try:
                qid = result["id"]
            except Exception as error:
                logging.warning("Error on qid, skipping item. Error: {0}".format(error))
                continue

            label = try_get_label_or_description(result, "labels", "en")
            subject_dict = {
                "id": qid,
                "label": label,
            }

            for langkey in languageKeys:
                label_lang = try_get_label_or_description(result, "labels", langkey)
                subject_dict.update({"label_" + langkey: label_lang})
            extract_dicts.append(subject_dict)

        item_count += len(chunk)
        print(f"Status of {type_name} labels: {item_count}/{len(qids)}")

    print(datetime.datetime.now(), f"Finished with {type_name} labels")
    return extract_dicts


already_extracted_superclass_ids = set()


def get_classes(
    type_name,
    qids,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    print(datetime.datetime.now(), f"Starting with {type_name}")
    if type_name == "classes":
        print(
            f"Total {type_name} to extract (only 'instance_of' of the provided qids): {len(qids)}"
        )
    else:
        print(
            f"Total {type_name} to extract (only 'subclass_of' of the provided qids): {len(qids)}"
        )
    item_count = 0
    extract_dicts = []
    chunk_size = 50  # The chunksize 50 is allowed by the wikidata api, bigger numbers need special permissions
    classes_id_chunks = util_funcs.chunks(list(qids), chunk_size)
    for chunk in classes_id_chunks:
        query_result = wikidata_entity_request(chunk)

        if "entities" not in query_result:
            logging.warn("Skipping chunk")
            continue

        for result in query_result["entities"].values():
            try:
                qid = result["id"]
            except Exception as error:
                logging.warning("Error on qid, skipping item. Error: {0}".format(error))

            label = try_get_label_or_description(result, "labels", "en")
            description = try_get_label_or_description(result, "descriptions", "en")
            subclass_of = try_get_qid_reference_list(
                result, property_name_to_property_id["subclass_of"]
            )
            class_dict = {
                "id": qid,
                "label": label,
                "description": description,
                "subclass_of": subclass_of,
            }

            for langkey in languageKeys:
                label_lang = try_get_label_or_description(result, "labels", langkey)
                description_lang = try_get_label_or_description(
                    result, "descriptions", langkey
                )
                class_dict.update(
                    {
                        "label_" + langkey: label_lang,
                        "description_" + langkey: description_lang,
                    }
                )
            extract_dicts.append(class_dict)

        item_count += len(chunk)
        print(f"Status of {type_name}: {item_count}/{len(qids)}")

    superclasses_qids = get_distinct_attribute_values_from_dict(
        "subclass_of", extract_dicts
    )
    missing_superclass_qids = []

    for superclass_id in superclasses_qids:
        if superclass_id not in already_extracted_superclass_ids:
            missing_superclass_qids.append(superclass_id)

    if len(missing_superclass_qids) == 0:
        return extract_dicts
    else:
        [
            already_extracted_superclass_ids.add(superclass_id)
            for superclass_id in superclasses_qids
        ]
        superclasses = get_classes("subclasses", missing_superclass_qids)
        for superclass in superclasses:
            extract_dicts.append(superclass)
        return extract_dicts


def get_unit_symbols(qids):
    print(datetime.datetime.now(), f"Starting with unit symbols")
    print(f"Total unit symbols to extract: {len(qids)}")
    item_count = 0
    extract_dicts = []
    chunk_size = 50  # The chunksize 50 is allowed by the wikidata api, bigger numbers need special permissions
    id_chunks = util_funcs.chunks(list(qids), chunk_size)
    for chunk in id_chunks:
        query_result = wikidata_entity_request(chunk, props=["claims"], timeout=10)

        if "entities" not in query_result:
            logging.warn("Skipping chunk")
            continue

        for result in query_result["entities"].values():
            try:
                qid = result["id"]
            except Exception as error:
                logging.warning("Error on qid, skipping item. Error: {0}".format(error))
                continue

            unit_symbol = try_get_unit_symbol(
                result, property_name_to_property_id["unit_symbol"]
            )

            subject_dict = {"id": qid, "unit_symbol": unit_symbol}
            extract_dicts.append(subject_dict)

        item_count += len(chunk)
        print(f"Status of unit symbols: {item_count}/{len(qids)}")

    print(datetime.datetime.now(), f"Finished with unit symbols")
    return extract_dicts


def resolve_unit_id_to_unit_symbol(artwork_dict, unit_symbols):
    attribute_names = ["height_unit", "width_unit", "length_unit", "diameter_unit"]
    qid_unit_symbol_dict = {}
    for unit_symbol_obj in unit_symbols:
        qid_unit_symbol_dict[unit_symbol_obj["id"]] = unit_symbol_obj

    for artwork_object in artwork_dict:
        for attribute_name in attribute_names:
            if artwork_object[attribute_name] != "":
                entity_id = artwork_object[attribute_name]
                artwork_object[attribute_name] = qid_unit_symbol_dict[entity_id][
                    "unit_symbol"
                ]
            else:
                artwork_object[attribute_name] = ""

    return artwork_dict


def resolve_entity_id_to_label(
    attribute_name,
    artwork_dict,
    labels,
    languageKeys=[item[0] for item in util_funcs.language_config_to_list()],
):
    # labels objects to qid_labels_dict
    qid_labels_dict = {}
    for label_obj in labels:
        qid_labels_dict[label_obj["id"]] = label_obj

    for artwork_object in artwork_dict:
        if artwork_object[attribute_name] != "":
            entity_id = artwork_object[attribute_name]
            artwork_object[attribute_name] = qid_labels_dict[entity_id]["label_en"]
            for langkey in languageKeys:
                artwork_object[f"{attribute_name}_{langkey}"] = qid_labels_dict[
                    entity_id
                ][f"label_{langkey}"]
        else:
            for langkey in languageKeys:
                artwork_object[f"{attribute_name}_{langkey}"] = ""

    return artwork_dict


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            DEV_CHUNK_LIMIT = int(sys.argv[2])
        print("DEV MODE: on, DEV_LIM={0}".format(DEV_CHUNK_LIMIT))
        DEV = True

    logging.debug("Extracting Art Ontology")
    extract_art_ontology()
