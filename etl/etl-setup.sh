#!/usr/bin/env bash

sudo apt-get install -y python3-virtualenv #installieren env.

virtualenv venv #env. erstellen und ordner erstellen

source venv/bin/activate #aktiviere fuer shell session env.

pip install -r requirements.txt #pakete aus datei lesen und installieren