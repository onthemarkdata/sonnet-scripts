import pytest
import os
import requests
import zipfile
from unittest import mock
from unittest.mock import MagicMock
from ingest_claims.load_claims_to_db import (
    download_file,
    extract_zip_file,
    rename_csv_file,
    cleanup_files,
)


@pytest.fixture
def temp_file(tmp_path):
    """Create a temp file for testing."""
    file = tmp_path / "test_file.txt"
    file.write_text("dummy content")
    return file


def test_download_file_success(mocker, tmp_path):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content = lambda chunk_size: [b"data"]

    mocker.patch("ingest_claims.load_claims_to_db.requests.get", return_value=mock_response)

    test_file = tmp_path / "test_download.zip"
    download_file("http://example.com/file.zip", test_file)

    assert os.path.exists(test_file)


def test_download_file_failure(mocker):
    """Test download failure handling."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch("ingest_claims.load_claims_to_db.requests.get", return_value=mock_response)

    with pytest.raises(Exception, match="Failed to download the file"):
        download_file("http://example.com/file.zip", "claims.zip")


def test_extract_zip_file(mocker, tmp_path):
    """Test zip extraction."""

    mock_zip = MagicMock()
    mock_zip.__enter__.return_value.namelist.return_value = ["test.csv"]
    mock_zip.__enter__.return_value.extractall = MagicMock()  # ✅ Add this!

    mocker.patch("ingest_claims.load_claims_to_db.zipfile.ZipFile", return_value=mock_zip)

    extracted_files = extract_zip_file("claims.zip", tmp_path)

    assert extracted_files == ["test.csv"]
    mock_zip.__enter__.return_value.extractall.assert_called_once_with(tmp_path)


def test_rename_csv_file_success(tmp_path):
    """Test renaming an existing CSV file."""
    original = tmp_path / "priginal.csv"
    renamed = tmp_path / "renamed.csv"

    original.write_text("test data")

    rename_csv_file(original, renamed)

    assert not original.exists()
    assert renamed.exists()


def test_rename_csv_file_missing():
    """Test renaming a missing file."""
    with pytest.raises(FileNotFoundError):
        rename_csv_file("missing.csv", "new.csv")


def test_cleanup_files(tmp_path):
    """Test cleanup removes files."""
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("data")
    file2.write_text("data")

    cleanup_files(file1, file2)

    assert not file1.exists()
    assert not file2.exists()
