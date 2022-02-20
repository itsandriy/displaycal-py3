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
    extensions = ["*.icc", "*.ti3"]
    d_files = {}
    for extension in extensions:
        # add files from DisplayCal/presets folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent / 'presets').glob(extension):
            d_files[element.name] = element

        # add files from DisplayCal/misc/ti3 folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent.parent / 'misc' / 'ti3').glob(extension):
            d_files[element.name] = element

    yield d_files
