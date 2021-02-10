import re


def sanitize(text: str):
    """
    This function removes linebreaks, carriage returns, duplicated spaces and all leading
    and trailing spaces from the passed string and returns the sanitized one. This function should be used
    for fields which contain longer strings like 'label' or 'term'.
    """
    # remove newline and carriage return
    sanitized_text = text.replace('\n', ' ').replace('\r', '')
    # remove duplicated spaces and remove leading and trailing spaces
    sanitized_text = re.sub(' +', ' ', sanitized_text)
    sanitized_text = sanitized_text.strip()

    return sanitized_text


def sanitize_id(id: str):
    """
    This funktion removed parenthesis and semicolons and qeestion marks from the passed string and
    remove spaces at the beginning and at the end of the string.Then replace spaces and commas
    with minus sign and returns the sanitized id.This function should be used
    for sanitizing id for all entities except location and icongraphy.
    """
    id = sanitize(id)

    # remove parenthesis and semicolons and qeestion marks
    remove_chars = ["(", ")", ";", "?"]
    for char in remove_chars:
        id = id.replace(char, "")

    # remove spaces at the beginning and at the end
    id = id.strip()

    # replace spaces and commas with minus sign
    replace_chars = [" ", ","]
    for char in replace_chars:
        id = id.replace(char, "-")

    return id


def get_id_by_prio(all_ids):
    """
    This funktion prioritize id and add the name of priority at the beginning of id with with minus sign
    to sanitize id and return only one of id according to priority.
    Priorities are first getty,gnd and term with
    """
    id = ""
    # Prio1: gett, Prio2: gnd, Prio3: term
    for current_type_id in all_ids:
        if 'getty' in current_type_id.text:
            id = "getty-" + current_type_id.text.split('/')[-1]
            break
        elif 'gnd' in current_type_id.text:
            id = "gnd-" + current_type_id.text.split('/')[-1]
            break
        elif 'term' in current_type_id.text:
            id = "ddk-" + current_type_id.text.split('/')[-1]
            break

    return sanitize_id(id)


def sanitize_location(location):

    remove_chars = ["-", "—", "(", ")", ";", "&", "?", "/", ",", "\"", "."]
    replace_chars = [" "]

    # remove special characters from a list
    for c in remove_chars:
        location = location.replace(c, "")

    location = sanitize(location)

    # replace spaces into minus sign
    for c in replace_chars:
        location = location.replace(c, "-")

    return location


def filter_none(json: dict):
    return {k: v for k, v in json.items() if v is not None}
