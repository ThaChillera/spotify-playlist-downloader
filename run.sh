#!/bin/bash

source venv/bin/activate
source secrets.sh

python downloader.py $(cat spotify_users.txt)
