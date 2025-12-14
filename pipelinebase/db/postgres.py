import psycopg2

import config
from db.validation import validate_identifier
from logging_config import setup_logging

logger = setup_logging(__name__)


def connect_to_db():
    """Connect to PostgreSQL database using configuration settings."""
    try:
        connection = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None


def copy_csv_to_db(conn, csv_file, table_name):
    """Copy CSV file data into a PostgreSQL table."""
    validate_identifier(table_name, "table name")

    with conn.cursor() as cur:
        with open(csv_file, "r") as file:
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", file)
        conn.commit()
        logger.info(f"Copied data from {csv_file} into the {table_name} table.")
