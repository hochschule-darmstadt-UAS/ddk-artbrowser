def sanitize(id): #TODO: ID-Format definieren, da auch mal Leerzeichen vorkommen können
    # Folgende Zeichen ersetzen: Leerzeichen, Klammern, &
    # Sonderzeichenliste definieren
    # Sonderzeichen ersetzen durch -
    return id

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

    return sanitize(id)