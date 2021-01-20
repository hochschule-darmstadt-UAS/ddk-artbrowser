#!/usr/bin/env bash

sudo apt-get install -y python3-virtualenv

# create virtual python environment in directory 'venv'
virtualenv venv

# activate virtual environment fpr current shell session
source venv/bin/activate

# install pip requirements into the virtual python environment
pip install -r requirements.txt