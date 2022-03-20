"""Sample DisplayData class."""
from typing import Dict, List

from wx import Rect


class DisplayData:
    """Sample Display."""

    DISPLAY_DATA_1 = {
        "name": b":1.0",
        "description": b"Monitor 1, Output DP-2 at 0, 0, width 1280, height 1024",
        "pos": (0, 0),
        "size": (1280, 1024),
        "size_mm": (338, 270),
        "x11_screen": 0,
        "screen": 0,
        "ramdac_screen": 0,
        "icc_profile_atom_id": 551,
        "edid": b"\x00\xff\xff\xff\xff\xff\xff\x00Zc:z\x0f\x01\x01\x011\x1e\x01\x04"
        b'\xb5<"x;\xb0\x91\xabRN\xa0&\x0fPT\xbf\xef\x80\xe1\xc0\xd1\x00\xd1\xc0'
        b"\xb3\x00\xa9@\x81\x80\x81\x00\x81\xc0V^\x00\xa0\xa0\xa0)P0 5\x00UP!"
        b"\x00\x00\x1a\x00\x00\x00\xff\x00W8U204900104\n\x00\x00\x00\xfd\x00"
        b"\x18K\x0fZ\x1e\x00\n      \x00\x00\x00\xfc\x00VP2768a\n     "
        b'\x01{\x02\x03"\xf1U\x90\x1f\x05\x14ZY\x04\x13\x1e\x1d\x0f\x0e\x07'
        b"\x06\x12\x11\x16\x15\x03\x02\x01#\t\x7f\x07\x83\x01\x00\x00\x02:"
        b"\x80\x18q8-@X,E\x00UP!\x00\x00\x1e\x01\x1d\x80\x18q\x1c\x16 X,%"
        b"\x00UP!\x00\x00\x9e\x02:\x80\xd0r8-@\x10,E\x80UP!\x00\x00\x1e\x01"
        b"\x1d\x00rQ\xd0\x1e n(U\x00UP!\x00\x00\x1eXM\x00\xb8\xa18\x14@\xf8,K"
        b"\x00UP!\x00\x00\x1e\x00\x00\x00\xd2",
        "output": 472,
        "icc_profile_output_atom_id": 551,
    }

    DISPLAY_DATA_2 = {
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

    CFG_DATA = [
        "Monitor 1, Output DP-2 @ 0, 0, 1280x1024",
    ]

    @property
    def Geometry(self) -> Rect:
        """Return a wx Rect as display geometry."""
        return Rect(
            self.DISPLAY_DATA_1["pos"][0],
            self.DISPLAY_DATA_1["pos"][1],
            self.DISPLAY_DATA_1["size"][0],
            self.DISPLAY_DATA_1["size"][1],
        )

    @staticmethod
    def enumerate_displays() -> List[Dict]:
        """Return the display data itself."""
        return [DisplayData.DISPLAY_DATA_1]
