import os
import requests
import zipfile

import pandas as pd

from db_utils import connect_to_db, create_claims_table, copy_csv_to_db

url = "http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.zip"

zip_file_name = "claims.zip"
csv_file_name = "claims.csv"


def download_file(url, zip_file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"{zip_file_name} downloaded successfully.")
    else:
        raise Exception(
            f"Failed to download the file. Status code: {response.status_code}"
        )

    return


def extract_zip_file(zip_file_name, extract_to="."):
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        extracted_files = zip_ref.namelist()
        print(f"Extraced files: {zip_ref.namelist()}")
    return extracted_files


def rename_csv_file(original_csv_name, csv_file_name):
    if os.path.exists(original_csv_name):
        os.rename(original_csv_name, csv_file_name)
        print(f"Renamed {original_csv_name} to {csv_file_name}.")
    else:
        raise FileNotFoundError(f"{original_csv_name} not found in extracted files.")


def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}.")
    return


def main():

    zip_file_name = "claims.zip"
    csv_file_name = "claims.csv"
    original_csv_name = "DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.csv"
    url = (
        "http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.zip"
    )

    db = None

    try:
        # Download the file
        download_file(url, zip_file_name)

        # Extract Zip File
        extract_zip_file(zip_file_name)
        rename_csv_file(original_csv_name, csv_file_name)
        cleanup_files(zip_file_name)

        # Connect to the Database
        print("Connecting to the database...")
        db = connect_to_db()

        with db.cursor() as cur:
            create_claims_table(cur)
            db.commit()

        # Copy the dataframe to the database
        print("Copying data to the database...")
        copy_csv_to_db(db, csv_file_name, "raw_claims")

        print("Data ingestion completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if db:
            db.rollback()
    finally:
        # Cleanup resources
        cleanup_files(csv_file_name)
        print("Removed the CSV file.")

        if db:
            print("Closing the database connection.")
            db.close()


if __name__ == "__main__":
    main()
