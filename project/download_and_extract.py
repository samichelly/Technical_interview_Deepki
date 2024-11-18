import requests
import gzip
import shutil
from pathlib import Path


def download_and_extract(url, gzipped_file_name):
    # Get the root directory of the project (parent of the current directory)
    parent_directory = (
        Path(__file__).resolve().parent.parent
    )  # Going up two levels to the project root

    # Path for the .gz file and the decompressed .csv file
    gzipped_file_path = parent_directory / gzipped_file_name
    extracted_file_path = parent_directory / gzipped_file_name.replace(
        ".gz", ""
    )  # Remove .gz to get the .csv

    # Download the .gz file
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(gzipped_file_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f"File downloaded successfully: {gzipped_file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return

    # Decompress the .gz file
    if gzipped_file_path.exists():
        print(f"Decompressing {gzipped_file_path}...")
        try:
            with gzip.open(gzipped_file_path, "rb") as f_in:
                with open(extracted_file_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"File decompressed successfully: {extracted_file_path}")
        except Exception as e:
            print(f"Error decompressing the file: {e}")
            return
    else:
        print(f"{gzipped_file_path} does not exist.")
