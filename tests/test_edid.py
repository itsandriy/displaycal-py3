# -*- coding: utf-8 -*-
from DisplayCAL import RealDisplaySizeMM, config
from DisplayCAL.dev.mocks import check_call
from tests.data.display_data import DisplayData
from DisplayCAL.edid import parse_edid


def test_get_edid_1():
    """Testing DisplayCAL.colord.device_id_from_edid() function."""
    from DisplayCAL.edid import get_edid

    RealDisplaySizeMM._displays = None
    assert RealDisplaySizeMM._displays is None
    with check_call(config, "getcfg", DisplayData.CFG_DATA, call_count=2):
        with check_call(
            RealDisplaySizeMM, "_enumerate_displays", DisplayData.enumerate_displays()
        ):
            result = get_edid(0)
    assert isinstance(result, dict)
    assert "blue_x" in result
    assert isinstance(result["blue_y"], float)
    assert "blue_y" in result
    assert isinstance(result["blue_y"], float)
    assert "checksum" in result
    assert result["checksum"] > 0
    assert "checksum_valid" in result
    assert result["checksum_valid"] is True
    assert "edid" in result
    assert isinstance(result["edid"], bytes)
    assert "edid_revision" in result
    assert isinstance(result["edid_revision"], int)
    assert "edid_version" in result
    assert isinstance(result["edid_version"], int)
    assert "ext_flag" in result
    assert isinstance(result["ext_flag"], int)
    assert "features" in result
    assert isinstance(result["features"], int)
    assert "gamma" in result
    assert isinstance(result["gamma"], float)
    assert "green_x" in result
    assert isinstance(result["green_x"], float)
    assert "green_y" in result
    assert isinstance(result["green_y"], float)
    assert "hash" in result
    assert isinstance(result["hash"], str)
    assert "header" in result
    assert isinstance(result["header"], bytes)
    assert "manufacturer" in result
    assert isinstance(result["manufacturer"], str)
    assert "manufacturer_id" in result
    assert isinstance(result["manufacturer_id"], str)
    assert "max_h_size_cm" in result
    assert isinstance(result["max_h_size_cm"], int)
    assert "max_v_size_cm" in result
    assert isinstance(result["max_v_size_cm"], int)
    assert "product_id" in result
    assert isinstance(result["product_id"], int)
    assert "red_x" in result
    assert isinstance(result["red_x"], float)
    assert "red_y" in result
    assert isinstance(result["red_y"], float)
    assert "serial_32" in result
    assert isinstance(result["serial_32"], int)
    assert "week_of_manufacture" in result
    assert isinstance(result["week_of_manufacture"], int)
    assert "white_x" in result
    assert isinstance(result["white_x"], float)
    assert "white_y" in result
    assert isinstance(result["white_y"], float)
    assert "year_of_manufacture" in result
    assert isinstance(result["year_of_manufacture"], int)


def test_parse_edid_1():
    """Testing DisplayCAL.edid.parse_edid() function."""
    raw_edid = (
        b"\x00\xff\xff\xff\xff\xff\xff\x00\x10\xac\xe0@L405\x05\x1b\x01\x04\xb57\x1fx:U"
        b"\xc5\xafO3\xb8%\x0bPT\xa5K\x00qO\xa9@\x81\x80\xd1\xc0\x01\x01\x01\x01\x01\x01"
        b"\x01\x01V^\x00\xa0\xa0\xa0)P0 5\x00)7!\x00\x00\x1a\x00\x00\x00\xff\x00"
        b"TYPR371U504L\n\x00\x00\x00\xfc\x00DELL UP2516D\n\x00\x00\x00\xfd\x002K\x1eX"
        b"\x19\x01\n      \x01,\x02\x03\x1c\xf1O\x90\x05\x04\x03\x02\x07\x16\x01\x06"
        b"\x11\x12\x15\x13\x14\x1f#\t\x1f\x07\x83\x01\x00\x00\x02:\x80\x18q8-@X,E"
        b"\x00)7!\x00\x00\x1e~9\x00\xa0\x808\x1f@0 :\x00)7!\x00\x00\x1a\x01\x1d\x00rQ"
        b"\xd0\x1e n(U\x00)7!\x00\x00\x1e\xbf\x16\x00\xa0\x808\x13@0 :\x00)7!\x00\x00"
        b"\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x86"
    )
    result = parse_edid(raw_edid)
    expected_result = {
        "blue_x": 0.1474609375,
        "blue_y": 0.04296875,
        "checksum": 44,
        "checksum_valid": True,
        "edid": b"\x00\xff\xff\xff\xff\xff\xff\x00\x10\xac\xe0@L405\x05\x1b\x01\x04"
        b"\xb57\x1fx:U\xc5\xafO3\xb8%\x0bPT\xa5K\x00qO\xa9@\x81\x80"
        b"\xd1\xc0\x01\x01\x01\x01\x01\x01\x01\x01V^\x00\xa0\xa0\xa0)P0 "
        b"5\x00)7!\x00\x00\x1a\x00\x00\x00\xff\x00TYPR371U504L\n\x00\x00"
        b"\x00\xfc\x00DELL UP2516D\n\x00\x00\x00\xfd\x002K\x1eX\x19\x01\n    "
        b"  \x01,\x02\x03\x1c\xf1O\x90\x05\x04\x03\x02\x07\x16\x01\x06\x11\x12"
        b"\x15\x13\x14\x1f#\t\x1f\x07\x83\x01\x00\x00\x02:\x80\x18q8-@X,E\x00"
        b")7!\x00\x00\x1e~9\x00\xa0\x808\x1f@0 :\x00)7!\x00\x00\x1a"
        b"\x01\x1d\x00rQ\xd0\x1e n(U\x00)7!\x00\x00\x1e\xbf\x16\x00\xa0\x808"
        b"\x13@0 :\x00)7!\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x86",
        "edid_revision": 4,
        "edid_version": 1,
        "ext_flag": 1,
        "features": 58,
        "gamma": 2.2,
        "green_x": 0.2001953125,
        "green_y": 0.7197265625,
        "hash": "40cf706d53476076b828fb8a78af796d",
        "header": b"\x00\xff\xff\xff\xff\xff\xff\x00",
        "manufacturer": "Dell, Inc.",
        "manufacturer_id": "DEL",
        "max_h_size_cm": 55,
        "max_v_size_cm": 31,
        "monitor_name": "DELL UP2516D",
        "product_id": 16608,
        "red_x": 0.6845703125,
        "red_y": 0.3095703125,
        "serial_32": 892351564,
        "serial_ascii": "TYPR371U504L",
        "week_of_manufacture": 5,
        "white_x": 0.3134765625,
        "white_y": 0.3291015625,
        "year_of_manufacture": 2017,
    }
    assert result == expected_result
