#!/usr/bin/env bash

source venv/bin/activate

python xml_importer/main.py

#Handle paths of input xml-files and output json files
#Run the xml-importer with theses input xml-files and store the json files
#Run the elasticsearch_uploader.py script with the generated json files.