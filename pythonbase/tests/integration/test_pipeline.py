import pytest
import psycopg2
import os
from ingest_claims.load_claims_to_db import main
from ingest_claims.db_utils import connect_to_db


@pytest.fixture(scope="module")
def test_db():
    """Fixture to set up and tear down a real test database."""
    os.environ["DB_HOST"] = "pgduckdb"
    conn = connect_to_db()
    yield conn
    conn.close()


def test_end_to_end_pipeline(test_db):
    """Test the full ingestion pipeline."""
    # Run the full pipeline
    main()

    # Verify that the raw_claims table contains data
    with test_db.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM raw_claims")
        result = cur.fetchone()
        assert result[0] > 0, "No data was inserted into raw_claims!"
