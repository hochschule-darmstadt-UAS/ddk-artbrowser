#!/usr/bin/env bash

mkdir -p /log_etl.log
LOG_FILE=/log_etl-setup.log

# this must be installed by a root/sudo user
#sudo apt-get install -y python3-virtualenv

# create virtual python environment in directory 'venv'
echo $(date -u) "INFO: Create virtual python environment in directory 'venv'" | ${LOG_FILE}
virtualenv venv

# activate virtual environment for current shell session
echo $(date -u) "INFO: Activate virtual environment for current shell session" | ${LOG_FILE}
source venv/bin/activate

# install pip requirements into the virtual python environment
echo $(date -u) "INFO: Install pip requirements into the virtual python environment" | ${LOG_FILE}
pip install -r requirements.txt

# create the input directory for the xml files
mkdir -p ./input
echo $(date -u) "INFO: Put your lido xml files into the directory ./input before running etl.sh" | ${LOG_FILE}
