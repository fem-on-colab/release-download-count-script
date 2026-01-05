# Copyright (C) 2022-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the release_download_count script."""

import importlib
import os
import sys
import types

import _pytest.fixtures
import pytest


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def release_download_count(root_directory: str) -> types.ModuleType:
    """Load the release_download_count module."""
    sys.path.insert(0, os.path.join(root_directory, "scripts"))
    release_download_count = importlib.import_module("release_download_count")
    sys.path.pop(0)
    return release_download_count


@pytest.fixture
def token(request: _pytest.fixtures.SubRequest) -> str:
    """Get token passed on the command line."""
    return request.config.getoption("--token")  # type: ignore[no-any-return]


def test_release_download_count(release_download_count: types.ModuleType, token: str) -> None:
    """
    Test the release_download_count function on the current repository.

    This test will fail in the (unlikely) case of a release asset being downloaded between the
    first and second "release_download_count" call.
    """
    dict_many_per_page = release_download_count.release_download_count(
        "fem-on-colab/release-download-count-script", token, 10)
    dict_one_per_page = release_download_count.release_download_count(
        "fem-on-colab/release-download-count-script", token, 1)

    assert dict_many_per_page == dict_one_per_page
    assert ("Initial commit", "test_file.txt") in dict_many_per_page
    assert dict_many_per_page[("Initial commit", "test_file.txt")] > 0
    assert ("Initial commit (copy)", "test_file_2.txt") in dict_many_per_page
    assert dict_many_per_page[("Initial commit (copy)", "test_file_2.txt")] > 0
    assert ("Initial commit (copy)", "test_file_3.txt") in dict_many_per_page
    assert dict_many_per_page[("Initial commit (copy)", "test_file_3.txt")] > 0
