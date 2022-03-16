# -*- coding: utf-8 -*-
from DisplayCAL.edid import get_edid


def test_device_id_from_edid_1():
    """Testing DisplayCAL.colord.device_id_from_edid() function."""
    from DisplayCAL.config import initcfg
    from DisplayCAL.colord import device_id_from_edid
    initcfg()
    edid = get_edid(0)
    device_id = device_id_from_edid(edid)
    assert isinstance(device_id, str)
    assert device_id != ""
