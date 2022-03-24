# -*- coding: utf-8 -*-
from DisplayCAL import argyll_cgats
from DisplayCAL import ICCProfile


def test_quote_nonoption_args_1():
    """Testing if the quote_nonoption_args() function is working properly."""
    test_value = [
        "/home/erkan.yilmaz/Downloads/Argyll_V2.3.0/bin/dispread",
        "-v",
        "-d1",
        "-c1",
        "-yn",
        "-P0.4711274060494959,1,1.0",
        "-k",
        "'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX.cal'",
        "'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX'",
    ]

    expected_result = [
        b'"/home/erkan.yilmaz/Downloads/Argyll_V2.3.0/bin/dispread"',
        b"-v",
        b"-d1",
        b"-c1",
        b"-yn",
        b"-P0.4711274060494959,1,1.0",
        b"-k",
        b"\"'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX.cal'\"",
        b"\"'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX'\"",
    ]

    result = argyll_cgats.quote_nonoption_args(test_value)
    assert result == expected_result


def test_vcgt_to_cal_1(data_files):
    """Testing the vcgt_to_cal() function."""
    icc_path = data_files["UP2516D #1 2022-03-23 16-06 D6500 2.2 F-S XYZLUT+MTX.icc"]
    profile = ICCProfile.ICCProfile(icc_path)
    cgats = argyll_cgats.vcgt_to_cal(profile)
    assert cgats[0]["COLOR_REP"] == b"RGB"
    assert cgats[0]["DATA_FORMAT"] == {
        0: b"RGB_I",
        1: b"RGB_R",
        2: b"RGB_G",
        3: b"RGB_B",
    }
    assert cgats[0]["DESCRIPTOR"] == b"Argyll Device Calibration State"
    assert cgats[0]["DEVICE_CLASS"] == b"DISPLAY"
    assert cgats[0]["KEYWORDS"] == {0: b"DEVICE_CLASS", 1: b"COLOR_REP", 2: b"RGB_I"}
    assert cgats[0]["ORIGINATOR"] == b"vcgt"


def test_extract_cal_from_profile_1(data_files):
    """Testing the extract_cal_from_profile() function."""
    icc_path = data_files["UP2516D #1 2022-03-23 16-06 D6500 2.2 F-S XYZLUT+MTX.icc"]
    profile = ICCProfile.ICCProfile(icc_path)
    cgats = argyll_cgats.extract_cal_from_profile(profile)
    assert cgats[0]["COLOR_REP"] == b"RGB"
    assert cgats[0]["DATA_FORMAT"] == {
        0: b"RGB_I",
        1: b"RGB_R",
        2: b"RGB_G",
        3: b"RGB_B",
    }
    assert cgats[0]["DESCRIPTOR"] == b"Argyll Device Calibration State"
    assert cgats[0]["DEVICE_CLASS"] == b"DISPLAY"
    assert cgats[0]["KEYWORDS"] == {0: b"DEVICE_CLASS", 1: b"COLOR_REP", 2: b"RGB_I"}
    assert cgats[0]["ORIGINATOR"] == b"vcgt"
