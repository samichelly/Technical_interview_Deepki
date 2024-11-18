#!/bin/bash

# Define the URL of the file to download
URL="https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/009_buildings.csv.gz"

# Define the name of the downloaded file
FILENAME="009_buildings.csv.gz"

# Download the file
echo "Downloading file $FILENAME..."
wget $URL -O $FILENAME

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download successful."

    # Decompress the .gz file
    echo "Decompressing file $FILENAME..."
    gunzip $FILENAME

    # Check if the decompression was successful
    if [ $? -eq 0 ]; then
        echo "Decompression successful. The file has been extracted to 009_buildings.csv."

        # Run the Python script
        echo "Running the Python script..."
        python3 -m project
    else
        echo "Error occurred while decompressing the file."
    fi
else
    echo "Error occurred during file download."
fi
