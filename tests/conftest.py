# -*- coding: utf-8 -*-

import pathlib
import pytest
import DisplayCAL


@pytest.fixture(scope="module")
def data_files():
    """generates data file list"""
    #  test/data
    extensions = ["*.txt", "*.tsv", "*.lin", "*.cal", "*.ti1", "*.ti3", "*.icc"]

    search_paths = [
        pathlib.Path(DisplayCAL.__file__).parent / "presets",
        pathlib.Path(DisplayCAL.__file__).parent.parent / "misc" / "ti3",
        pathlib.Path(DisplayCAL.__file__).parent.parent / "tests" / "data",
        pathlib.Path(DisplayCAL.__file__).parent.parent / "tests" / "data" / "sample",
        pathlib.Path(DisplayCAL.__file__).parent,
        pathlib.Path(DisplayCAL.__file__).parent / "ti1",
    ]
    d_files = {}
    for path in search_paths:
        for extension in extensions:
            # add files from DisplayCal/presets folder
            for element in path.glob(extension):
                d_files[element.name] = element

    yield d_files
