# -*- coding: utf-8 -*-

from DisplayCAL import RealDisplaySizeMM, config
from DisplayCAL.dev.mocks import check_call
from tests.data.display_data import DisplayData


def test_get_default_size_1():
    """Testing wxMeasureFrame.get_default_size() function."""
    from DisplayCAL.config import initcfg
    from DisplayCAL.wxMeasureFrame import get_default_size

    initcfg()
    import wx

    app = wx.GetApp()
    if not app:
        app = wx.PySimpleApp()
    with check_call(
        RealDisplaySizeMM, "_enumerate_displays", DisplayData.enumerate_displays()
    ):
        with check_call(config, "getcfg", DisplayData.CFG_DATA, call_count=24):
            result = get_default_size()
    assert isinstance(result, int)
    assert result > 1
