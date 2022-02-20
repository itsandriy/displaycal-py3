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
    extensions = ["*.icc"]
    d_files = {}
    for extension in extensions:
        # add files from DisplayCal/presets folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent / 'presets').glob(extension):
            d_files[element.name] = element

    yield d_files
