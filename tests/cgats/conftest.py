# -*- coding: utf-8 -*-

import pathlib
import pytest
import DisplayCAL


HERE = pathlib.Path(__file__).parent


@pytest.fixture(scope="module")
def data_files():
    """generates data file list
    """
    #  test/data
    extensions = ["*.txt", "*.tsv", "*.lin", "*.cal", "*.ti1", "*.ti3"]
    d_files = {}
    for extension in extensions:
        # add files from "tests/cgats/data" folder
        for element in (HERE / "data").glob(extension):
            d_files[element.name] = element

        # add files from DisplayCal folder
        for element in pathlib.Path(DisplayCAL.__file__).parent.glob(extension):
            d_files[element.name] = element

        # add files from DisplayCal.ti1 folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent / 'ti1').glob(extension):
            d_files[element.name] = element

    yield d_files
