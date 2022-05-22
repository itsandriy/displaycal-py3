# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import pytest

from DisplayCAL import argyll_cgats
from DisplayCAL import ICCProfile
from DisplayCAL.CGATS import CGATS
from DisplayCAL.debughelpers import Error


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


@pytest.mark.parametrize(
    "icc_name,exception",
    (
        ("UP2516D #1 2022-03-23 16-06 D6500 2.2 F-S XYZLUT+MTX.icc", False),
        ("vcgt_cm_test_yellowish_blueish.icc", False),
        ("BenQ PD2700U-AC19BB79-F553-4582-B898-4247D669C2F1.icc", True),
    ),
)
def test_extract_cal_from_profile_1(data_files, icc_name: str, exception: bool) -> None:
    """Testing the extract_cal_from_profile() function."""
    icc_path = data_files[icc_name]
    profile = ICCProfile.ICCProfile(icc_path)
    if exception:
        with pytest.raises(Error):
            argyll_cgats.extract_cal_from_profile(profile)
    else:
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
        assert cgats[0]["KEYWORDS"] == {
            0: b"DEVICE_CLASS",
            1: b"COLOR_REP",
            2: b"RGB_I",
        }
        assert cgats[0]["ORIGINATOR"] == b"vcgt"


@pytest.mark.parametrize(
    "profile, result",
    (
        ("0_16_proper.ti3", b"CTI1"),
        ("BenQ PD2700U-AC19BB79-F553-4582-B898-4247D669C2F1.icc", None),
    ),
)
def test_ti3_to_ti1(data_files, profile: str, result: bytes | None) -> None:
    """Testing the ti3_to_ti1() function."""
    path = data_files[profile]
    if not result:
        assert not argyll_cgats.ti3_to_ti1(path)
    else:
        assert result in argyll_cgats.ti3_to_ti1(path)


@pytest.mark.parametrize("gray", (True, False), ids=("with gray", "without gray"))
@pytest.mark.parametrize(
    "include_neutrals",
    (True, False),
    ids=("include neutrals", "don't include neutrals"),
)
@pytest.mark.parametrize(
    "profile, sets",
    (
        ("0_16_proper.ti3", (3, 2, 0, 1)),
        ("Monitor_AllBlack.ti3", (52, 120, 120, 167)),
    ),
)
def test_extract_device_gray_primaries(
    data_files,
    profile: str,
    sets: Tuple[int, int, int, int],
    include_neutrals: bool,
    gray: bool,
) -> None:
    """Testing the extract_device_gray_primaries() function."""
    path = data_files[profile]
    cgats = CGATS(cgats=path)
    (
        ti3_extracted,
        RGB_XYZ_extracted,
        RGB_XYZ_remaining,
    ) = argyll_cgats.extract_device_gray_primaries(
        cgats, include_neutrals=include_neutrals, gray=gray
    )
    assert len(ti3_extracted) == 4
    assert len(RGB_XYZ_extracted) == sets[0] if gray else sets[1]
    assert len(RGB_XYZ_remaining) == sets[2] if gray else sets[3]
