# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.

"""Tests for Asset"""

import os
import tempfile

import pytest

from covalent_dispatcher._dal.asset import (
    Asset,
    InvalidFileExtension,
    StorageType,
    load_file,
    store_file,
)
from covalent_dispatcher._db import models
from covalent_dispatcher._db.datastore import DataStore


@pytest.fixture
def test_db():
    """Instantiate and return an in-memory database."""

    return DataStore(
        db_URL="sqlite+pysqlite:///:memory:",
        initialize_db=True,
    )


def get_asset_record(storage_path, object_key, digest_alg="", digest=""):
    return models.Asset(
        storage_type=StorageType.LOCAL,
        storage_path=storage_path,
        object_key=object_key,
        digest_alg=digest_alg,
        digest=digest,
    )


def test_asset_load_data():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as temp:
        temp.write("Hello\n")
        temppath = temp.name
        key = os.path.basename(temppath)

    storage_path = "/tmp"

    rec = get_asset_record(storage_path, key)
    a = Asset(None, rec)
    assert a.load_data() == "Hello\n"
    os.unlink(temppath)


def test_asset_store_data():
    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as temp:
        temppath = temp.name
        key = os.path.basename(temppath)
    storage_path = "/tmp"
    rec = get_asset_record(storage_path, key)
    a = Asset(None, rec)
    a.store_data("Hello\n")

    with open(temppath, "r") as f:
        assert f.read() == "Hello\n"

    os.unlink(temppath)


def test_upload_asset():
    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as temp:
        src_path = temp.name
        src_key = os.path.basename(src_path)
    storage_path = "/tmp"

    rec = get_asset_record(storage_path, src_key)
    a = Asset(None, rec)
    a.store_data("Hello\n")

    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as temp:
        dest_path = temp.name
        dest_key = os.path.basename(dest_path)

    a.upload(dest_path)

    with open(dest_path, "r") as f:
        assert f.read() == "Hello\n"
    os.unlink(dest_path)


def test_download_asset():
    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as temp:
        src_path = temp.name
        src_key = os.path.basename(src_path)
    with open(src_path, "w") as f:
        f.write("Hello\n")

    storage_path = "/tmp"
    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as temp:
        dest_path = temp.name
        dest_key = os.path.basename(dest_path)

    rec = get_asset_record(storage_path, dest_key)
    a = Asset(None, rec)

    a.download(src_path)

    assert a.load_data() == "Hello\n"

    os.unlink(dest_path)


# Moved from write_result_to_db_test.py


def test_store_file_invalid_extension():
    """Test the function used to write data corresponding to the filenames in the DB."""

    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.invalid", data="")

        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.txt", data={4})

        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.log", data={4})


def test_store_file_valid_extension():
    """Test the function used to write data corresponding to the filenames in the DB."""

    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.invalid", data="")

        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.txt", data={4})

        with pytest.raises(InvalidFileExtension):
            store_file(storage_path=temp_dir, filename="test.log", data={4})


def test_store_and_load_file():
    """Test the data storage and loading methods simultaneously."""

    with tempfile.TemporaryDirectory() as temp_dir:
        data = [1, 2, 3]
        store_file(storage_path=temp_dir, filename="pickle.pkl", data=data)
        assert load_file(storage_path=temp_dir, filename="pickle.pkl") == data

        data = None
        store_file(storage_path=temp_dir, filename="pickle.txt", data=data)
        assert load_file(storage_path=temp_dir, filename="pickle.txt") == ""
