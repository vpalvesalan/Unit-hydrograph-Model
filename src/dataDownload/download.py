import requests
import zipfile
import os
from pathlib import Path
import sys

# Add src to system path
sys.path.append(str(Path.cwd().parent))

# import modules
from utils.utils import measure_execution_time

@measure_execution_time
def download(url: str, filename: str, unzip: bool = False, deleteZip = True, chunk_size: int = 8192) -> None:
    """
    Downloads a file from a URL and optionally extracts it if it's a ZIP file.

    Parameters:
        url (str): The URL of the file to download.
        filename (str): The local filename to save the downloaded file as.
        unzip (bool): Whether to extract the file if it's a ZIP file. Default is False.
        chunk_size (int): The size of chunks for streaming downloads. Default is 8192 bytes.
        deleteZip (bool): Wether to dele zipped files after extracted.

    """
    try:
        filename_print = os.path.basename(filename)
        print(f'Downloading file {filename_print}')

        # Download the file with streaming for large files
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {filename_print}")

        # Unzip file
        if unzip:
            file_base_name = os.path.splitext(os.path.basename(filename))[0]
            extract_directory = Path(filename).parent / file_base_name
            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall(extract_directory)
                print(f"Extracted files to: {extract_directory}")
                
                # Delete the ZIP file after extraction
                if deleteZip:
                    os.remove(filename)
                    print(f"Deleted ZIP file: {filename}")
                    
            except zipfile.BadZipFile:
                print(f"Error: {filename} is not a valid ZIP file.")
    except requests.RequestException as e:
        print(f"Download failed: {e}")
    except OSError as e:
        print(f"File operation failed: {e}")
