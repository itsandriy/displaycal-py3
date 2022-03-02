# -*- coding: utf-8 -*-

import pathlib
import pytest
import DisplayCAL


@pytest.fixture(scope="module")
def data_files():
    """generates data file list"""
    #  test/data
    extensions = ["*.txt", "*.tsv", "*.lin", "*.cal", "*.ti1", "*.ti3", "*.icc"]
    d_files = {}
    for extension in extensions:
        # add files from DisplayCal/presets folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent / "presets").glob(
            extension
        ):
            d_files[element.name] = element

        # add files from DisplayCal/misc/ti3 folder
        for element in (
            pathlib.Path(DisplayCAL.__file__).parent.parent / "misc" / "ti3"
        ).glob(extension):
            d_files[element.name] = element

        # add files from "tests/cgats/data" folder
        for element in (
            pathlib.Path(DisplayCAL.__file__).parent.parent / "tests" / "cgats" / "data"
        ).glob(extension):
            d_files[element.name] = element

        # add files from DisplayCal folder
        for element in pathlib.Path(DisplayCAL.__file__).parent.glob(extension):
            d_files[element.name] = element

        # add files from DisplayCal.ti1 folder
        for element in (pathlib.Path(DisplayCAL.__file__).parent / "ti1").glob(
            extension
        ):
            d_files[element.name] = element

    yield d_files
