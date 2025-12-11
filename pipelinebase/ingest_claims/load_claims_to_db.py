import os
import requests
import zipfile

import config
from db.postgres import connect_to_db, copy_csv_to_db
from ingest_claims.schema import create_claims_table
from logging_config import setup_logging

logger = setup_logging(__name__)


def download_file(url, zip_file_name):
    """Download a file from a URL."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.info(f"{zip_file_name} downloaded successfully.")
    else:
        raise Exception(
            f"Failed to download the file. Status code: {response.status_code}"
        )


def extract_zip_file(zip_file_name, extract_to="."):
    """Extract a zip file to the specified directory."""
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        extracted_files = zip_ref.namelist()
        logger.info(f"Extracted files: {zip_ref.namelist()}")
    return extracted_files


def rename_csv_file(original_csv_name, csv_file_name):
    """Rename a CSV file."""
    if os.path.exists(original_csv_name):
        os.rename(original_csv_name, csv_file_name)
        logger.info(f"Renamed {original_csv_name} to {csv_file_name}.")
    else:
        raise FileNotFoundError(f"{original_csv_name} not found in extracted files.")


def cleanup_files(*files):
    """Remove specified files."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logger.debug(f"Removed {file}.")


def main():
    db = None

    try:
        # Download the file
        download_file(config.CLAIMS_URL, config.CLAIMS_ZIP_FILE)

        # Extract Zip File
        extract_zip_file(config.CLAIMS_ZIP_FILE)
        rename_csv_file(config.CLAIMS_ORIGINAL_CSV, config.CLAIMS_CSV_FILE)
        cleanup_files(config.CLAIMS_ZIP_FILE)

        # Connect to the Database
        logger.info("Connecting to the database...")
        db = connect_to_db()

        with db.cursor() as cur:
            create_claims_table(cur)
            db.commit()

        # Copy the dataframe to the database
        logger.info("Copying data to the database...")
        copy_csv_to_db(db, config.CLAIMS_CSV_FILE, "raw_claims")

        logger.info("Data ingestion completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if db:
            db.rollback()
    finally:
        logger.debug("Not removing the CSV file.")

        if db:
            logger.info("Closing the database connection.")
            db.close()


if __name__ == "__main__":
    main()
