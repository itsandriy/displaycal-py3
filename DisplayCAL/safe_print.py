# -*- coding: utf-8 -*-

import locale
import os
import sys

from encoding import get_encoding, get_encodings
from util_str import safe_unicode

original_codepage = None

enc, fs_enc = get_encodings()


_conwidth = None

def _get_console_width():
    global _conwidth
    if _conwidth is None:
        _conwidth = 80
        try:
            if sys.platform == "win32":
                from ctypes import windll, create_string_buffer
                import struct
                # Use stderr handle so that pipes don't affect the reported size
                stderr_handle = windll.kernel32.GetStdHandle(-12)
                buf = create_string_buffer(22)
                consinfo = windll.kernel32.GetConsoleScreenBufferInfo(stderr_handle,
                                                                      buf)
                if consinfo:
                    _conwidth = struct.unpack("hhhhHhhhhhh", buf.raw)[0]
            else:
                _conwidth = int(os.getenv("COLUMNS"))
        except:
            pass
    return _conwidth


safe_print = print


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        safe_print(arg.decode(fs_enc))
