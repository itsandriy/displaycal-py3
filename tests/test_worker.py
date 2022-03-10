# -*- coding: utf-8 -*-

import io

import pytest

from DisplayCAL.worker import make_argyll_compatible_path, Worker


# todo: deactivated test temporarily
# def test_get_options_from_profile_is_working_properly(data_files):
#     """testing if ``DisplayCAL.worker.get_options_from_profile()`` is working properly
#     """
#     from DisplayCAL.worker import get_options_from_profile
#     options = get_options_from_profile(profile=data_files["default.ti3"].absolute())


def test_make_argyll_compatible_path_1():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = "C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = "C_Program Files_some path_excutable.exe"
    assert result == expected_result


def test_make_argyll_compatible_path_2():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = b"C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = b"C_Program Files_some path_excutable.exe"
    assert result == expected_result


def test_worker_get_instrument_name_1():
    """testing if the Worker.get_instrument_name() is working properly"""
    worker = Worker()
    result = worker.get_instrument_name()
    expected_result = ""
    assert result == expected_result


def test_worker_get_instrument_features():
    """testing if Worker.get_instrument_features() is working properly"""
    worker = Worker()
    result = worker.get_instrument_features()
    assert result == {}


def test_worker_instrument_supports_css_1():
    """testing if Worker.instrument_supports_ccss is working properly"""
    worker = Worker()
    result = worker.instrument_supports_ccss()
    expected_result = None
    assert result == expected_result


def test_generate_b2a_from_inverse_table(data_files, argyll):
    """Test Worker.generate_B2A_from_inverse_table() method"""
    if not argyll:
        # just skip this test so that it doesn't generate error on GitHub
        pytest.skip("Cannot find argyll")

    worker = Worker()
    from DisplayCAL import ICCProfile

    icc_profile1 = ICCProfile.ICCProfile(
        profile=data_files[
            "Monitor 1 #1 2022-03-09 16-13 D6500 2.2 F-S XYZLUT+MTX.icc"
        ].absolute()
    )
    logfile = io.StringIO()
    result = worker.generate_B2A_from_inverse_table(icc_profile1, logfile=logfile)
    assert result is True
