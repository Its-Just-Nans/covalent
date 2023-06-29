# Copyright 2023 Agnostiq Inc.
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

"""Unit tests for the importer entry point"""

from unittest.mock import MagicMock

import pytest

from covalent_dispatcher._core.data_modules.importer import (
    _copy_assets,
    import_derived_manifest,
    import_manifest,
)


@pytest.mark.asyncio
async def test_import_manifest(mocker):
    mock_manifest = MagicMock()
    mock_manifest.metadata.dispatch_id = None

    mock_srvres = MagicMock()
    mocker.patch(
        "covalent_dispatcher._dal.result.Result.from_dispatch_id", return_value=mock_srvres
    )

    mock_asset = MagicMock()
    mock_asset.remote_uri = "s3://mybucket/object.pkl"

    mocker.patch(
        "covalent_dispatcher._core.data_modules.importer.import_result", return_value=mock_manifest
    )

    mock_assets = {"lattice": [mock_asset], "nodes": [mock_asset]}
    mocker.patch(
        "covalent_dispatcher._core.data_modules.importer._get_all_assets", return_value=mock_assets
    )

    return_manifest = await import_manifest(mock_manifest, None, None)

    assert return_manifest.metadata.dispatch_id is not None


@pytest.mark.asyncio
async def test_import_sublattice_manifest(mocker):
    mock_manifest = MagicMock()
    mock_manifest.metadata.dispatch_id = None

    mock_parent_res = MagicMock()
    mock_parent_res.root_dispatch_id = "parent_dispatch_id"

    mock_asset = MagicMock()
    mock_asset.remote_uri = "s3://mybucket/object.pkl"

    mock_srvres = MagicMock()
    mocker.patch(
        "covalent_dispatcher._dal.result.Result.from_dispatch_id", return_value=mock_parent_res
    )

    mocker.patch(
        "covalent_dispatcher._core.data_modules.importer.import_result", return_value=mock_manifest
    )

    mock_assets = {"lattice": [MagicMock()], "nodes": [MagicMock()]}

    return_manifest = await import_manifest(mock_manifest, "parent_dispatch_id", None)

    assert return_manifest.metadata.dispatch_id is not None
    assert return_manifest.metadata.root_dispatch_id == "parent_dispatch_id"


@pytest.mark.asyncio
async def test_import_derived_manifest(mocker):
    mock_manifest = MagicMock()
    mock_manifest.metadata.dispatch_id = "test_import_derived_manifest"

    mock_import_manifest = mocker.patch(
        "covalent_dispatcher._core.data_modules.importer._import_manifest",
    )

    mock_copy = mocker.patch(
        "covalent_dispatcher._core.data_modules.importer._copy_assets",
    )

    mock_handle_redispatch = mocker.patch(
        "covalent_dispatcher._core.data_modules.importer.handle_redispatch",
        return_value=(mock_manifest, []),
    )

    mock_pull = mocker.patch(
        "covalent_dispatcher._core.data_modules.importer._pull_assets",
    )

    mock_manifest = {}
    await import_derived_manifest(mock_manifest, "parent_dispatch", True)

    mock_import_manifest.assert_called()
    mock_pull.assert_called()
    mock_handle_redispatch.assert_called()
    mock_copy.assert_called_with([])


def test_copy_assets(mocker):
    mock_copy = mocker.patch("covalent_dispatcher._core.data_modules.importer.copy_asset")

    _copy_assets([("src", "dest")])
    mock_copy.assert_called_with("src", "dest")
