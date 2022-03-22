# -*- coding: utf-8 -*-
import codecs

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


def test_parse_edid_2():
    """Testing DisplayCAL.edid.parse_edid() function. for #50"""
    xrandr_edid_data = """
                00ffffffffffff0004725805436e6072
                1a1b0103805e35782aa191a9544d9c26
                0f5054bfef80714f8140818081c08100
                9500b300d1c04dd000a0f0703e803020
                3500ad113200001a565e00a0a0a02950
                2f203500ad113200001a000000fd0032
                3c1e8c3c000a202020202020000000fc
                00416365722045543433304b0a200129
                020341f1506101600304121305141f10
                0706026b5f23090707830100006b030c
                002000383c2000200167d85dc4017880
                00e305e001e40f050000e60607016060
                45023a801871382d40582c4500ad1132
                00001e011d007251d01e206e285500ad
                113200001e8c0ad08a20e02d10103e96
                00ad1132000018000000000000000088"""
    xrandr_edid_data = "".join(xrandr_edid_data.split("\n")).replace(" ", "").strip()
    raw_edid = codecs.decode(xrandr_edid_data, "hex")
    result = parse_edid(raw_edid)
    expected_result = {
        "blue_x": 0.150390625,
        "blue_y": 0.0595703125,
        "checksum": 41,
        "checksum_valid": True,
        "edid": b"\x00\xff\xff\xff\xff\xff\xff\x00\x04rX\x05Cn`r\x1a\x1b\x01\x03"
        b"\x80^5x*\xa1\x91\xa9TM\x9c&\x0fPT\xbf\xef\x80qO\x81@\x81\x80"
        b"\x81\xc0\x81\x00\x95\x00\xb3\x00\xd1\xc0M\xd0\x00\xa0\xf0p>\x800 "
        b"5\x00\xad\x112\x00\x00\x1aV^\x00\xa0\xa0\xa0)P/ 5\x00\xad\x112\x00"
        b"\x00\x1a\x00\x00\x00\xfd\x002<\x1e\x8c<\x00\n      \x00\x00\x00\xfc"
        b"\x00Acer ET430K\n \x01)\x02\x03A\xf1Pa\x01`\x03\x04\x12\x13"
        b"\x05\x14\x1f\x10\x07\x06\x02k_#\t\x07\x07\x83\x01\x00\x00k\x03\x0c"
        b"\x00 \x008< \x00 \x01g\xd8]\xc4\x01x\x80\x00\xe3\x05\xe0"
        b"\x01\xe4\x0f\x05\x00\x00\xe6\x06\x07\x01``E\x02:\x80\x18q8-@X,E"
        b"\x00\xad\x112\x00\x00\x1e\x01\x1d\x00rQ\xd0\x1e n(U\x00\xad"
        b"\x112\x00\x00\x1e\x8c\n\xd0\x8a \xe0-\x10\x10>\x96\x00\xad\x112"
        b"\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x88",
        "edid_revision": 3,
        "edid_version": 1,
        "ext_flag": 1,
        "features": 42,
        "gamma": 2.2,
        "green_x": 0.30078125,
        "green_y": 0.6103515625,
        "hash": "23d07c7921998829a4b68374e1000cfe",
        "header": b"\x00\xff\xff\xff\xff\xff\xff\x00",
        "manufacturer": "Acer Technologies",
        "manufacturer_id": "ACR",
        "max_h_size_cm": 94,
        "max_v_size_cm": 53,
        "monitor_name": "Acer ET430K",
        "product_id": 1368,
        "red_x": 0.662109375,
        "red_y": 0.330078125,
        "serial_32": 1918922307,
        "week_of_manufacture": 26,
        "white_x": 0.3125,
        "white_y": 0.3291015625,
        "year_of_manufacture": 2017,
    }
    assert result == expected_result
