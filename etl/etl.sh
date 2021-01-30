#!/usr/bin/env bash

mkdir -p /log_etl.log
LOG_FILE=/log_etl.log

if [ -f ./venv ] ;then

echo $(date -u) "INFO: Use the virtual python environment: source venv/bin/activate" | ${LOG_FILE}
source venv/bin/activate

echo $(date -u) "INFO: Handle paths of input xml-files and output json files" | ${LOG_FILE}
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

mkdir -p ./output

echo $(date -u) "INFO: Run the xml-importer with theses input xml-files and store the json files" | ${LOG_FILE}
python xml_importer/main.py ./input ./output

echo $(date -u) "INFO: Run the elasticsearch_uploader.py script with the generated json files." | ${LOG_FILE}
python upload_to_elasticsearch/elasticsearch_uploader.py ./output

else
echo $(date -u) "ERROR: folder venv not available. Please run first etl-setup.sh" | ${LOG_FILE}
exit 1;
fi





