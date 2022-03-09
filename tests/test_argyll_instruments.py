# -*- coding: utf-8 -*-
from DisplayCAL.CGATS import CGATS
from DisplayCAL.argyll_instruments import (
    get_canonical_instrument_name,
    remove_vendor_names,
)


def test_get_canonical_instrument_name_1(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with no replacement."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(target_instrument)
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_2(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            "DTP94-LCD mode": "DTP94",
            "eye-one display": "i1 Display",
            "Spyder 2 LCD": "Spyder2",
            "Spyder 3": "Spyder3",
        },
    )
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_3(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            b"DTP94-LCD mode": b"DTP94",
            b"eye-one display": b"i1 Display",
            b"Spyder 2 LCD": b"Spyder2",
            b"Spyder 3": b"Spyder3",
        },
    )
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_4(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            b"DTP94-LCD mode": "DTP94",
            b"eye-one display": "i1 Display",
            b"Spyder 2 LCD": "Spyder2",
            b"Spyder 3": "Spyder3",
        },
    )
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_5(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            "DTP94-LCD mode": b"DTP94",
            "eye-one display": b"i1 Display",
            "Spyder 2 LCD": b"Spyder2",
            "Spyder 3": b"Spyder3",
        },
    )
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_6(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT").decode("utf-8")
    assert target_instrument == "X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            b"DTP94-LCD mode": "DTP94",
            b"eye-one display": "i1 Display",
            b"Spyder 2 LCD": "Spyder2",
            b"Spyder 3": "Spyder3",
        },
    )
    expected_result = "i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_get_canonical_instrument_name_7(data_files):
    """Test argyll_instruments.get_canonical_instrument_name() with replacement dict."""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT").decode("utf-8")
    assert target_instrument == "X-Rite i1 DisplayPro, ColorMunki Display"
    result = get_canonical_instrument_name(
        target_instrument,
        {
            "DTP94-LCD mode": b"DTP94",
            "eye-one display": b"i1 Display",
            "Spyder 2 LCD": b"Spyder2",
            "Spyder 3": b"Spyder3",
        },
    )
    expected_result = "i1 DisplayPro, ColorMunki Display"
    assert result == expected_result


def test_remove_vendor_names(data_files):
    """testing the argyll_instruments.remove_vendor_names() function"""
    path = data_files["0_16.ti3"]
    cgats = CGATS(path)
    target_instrument = cgats.queryv1("TARGET_INSTRUMENT")
    assert target_instrument == b"X-Rite i1 DisplayPro, ColorMunki Display"
    result = remove_vendor_names(target_instrument)
    expected_result = b"i1 DisplayPro, ColorMunki Display"
    assert result == expected_result
