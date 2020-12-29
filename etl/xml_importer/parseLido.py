import re


def sanitize_id(id): #TODO: ID-Format definieren, da auch mal Leerzeichen vorkommen können
    spec_char = ["(", ")"] #Special character list, you can add new char's
    for char in spec_char:
        id = id.replace(char, "-")

    id = id.strip()

    return id


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


def get_id_by_prio(all_ids):
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


def sanitize_location(location): ##TODO: Method besser definieren
    spec_char = [" — ", " / ", " "]
    spec_char2 = ["(", ")"]
    for char in spec_char:
        location = location.replace(char, "-")
    for char2 in spec_char2:
        location = location.replace(char2, "")
    return location


