#!/usr/bin/env bash

sudo apt-get install -y python3-virtualenv

# create virtual python environment in directory 'venv'
virtualenv venv

# activate virtual environment for current shell session
source venv/bin/activate

# install pip requirements into the virtual python environment
pip install -r requirements.txt

# create the input directory for the xml files
mkdir -p ./input
echo "Put your lido xml files into the directory ./input before running etl.sh"