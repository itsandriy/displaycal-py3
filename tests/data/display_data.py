"""Sample DisplayData class."""
from typing import Dict, List


class DisplayData:
    """Sample Display."""

    DISPLAY_DATA = {
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

    CFG_DATA = [
        "Monitor 1, Output DP-2 @ 0, 0, 1280x1024",
    ]

    @staticmethod
    def enumerate_displays() -> List[Dict]:
        """Return the display data itself."""
        return [DisplayData.DISPLAY_DATA]
