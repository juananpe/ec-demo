#!/bin/bash

# Loop through all json (.json) files in the current directory
for jsonfile in *.json; do
    # Check if the file is a regular file
    if [ -f "$jsonfile" ]; then
        python ../ingest_json_file.py  "$jsonfile"  "../ec_app.yaml"
    fi
done