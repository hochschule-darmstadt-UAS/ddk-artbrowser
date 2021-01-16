#!/usr/bin/env bash

source venv/bin/activate

export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

mkdir -p ./output

python xml_importer/main.py ./input ./output

python upload_to_elasticsearch/elasticsearch_uploader.py ./output