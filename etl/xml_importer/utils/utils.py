import logging


def setup_logger(logger_name: str, filename: str):
    """Setup a logger for a python script.
    The root logging object is created within this helper script.
    Args:
        logger_name: Package + module name e.g. 'data_extraction.get_wikidata_items'
        filename: String to the path and file the logger writes to

    Returns:
        Logger object
    """
    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    date_format = "%d.%m.%Y %H:%M"
    file_formatter = logging.Formatter(format, date_format)
    console_formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")

    logger = logging.getLogger(logger_name)

    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Print warnings and errors to console
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
