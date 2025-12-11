import pytest
import psycopg2
from unittest import mock
from unittest.mock import MagicMock

from db.postgres import connect_to_db
from ingest_claims.schema import create_claims_table


@pytest.fixture
def mock_cursor():
    """Fixture for a mocked database cursor."""
    return MagicMock()


@pytest.fixture
def mock_conn(mock_cursor):
    """Fixture for a mocked database connection."""
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn


def test_connect_to_db_success():
    """Test that connect_to_db successfully connects using a mock."""
    with mock.patch("db.postgres.psycopg2.connect", return_value=MagicMock()) as mock_connect:
        conn = connect_to_db()
        assert conn is not None
        mock_connect.assert_called_once()


def test_connect_to_db_failure():
    """Test the connect_to_db returns None if connection fails."""
    with mock.patch("db.postgres.psycopg2.connect", side_effect=psycopg2.OperationalError):
        conn = connect_to_db()
        assert conn is None


def test_create_claims_table(mock_conn, mock_cursor):
    """Test that create_claims_table executes a SQL query."""
    create_claims_table(mock_cursor)
    mock_cursor.execute.assert_called_once()
    assert (
        "CREATE TABLE IF NOT EXISTS raw_claims" in mock_cursor.execute.call_args[0][0]
    )
