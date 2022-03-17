# -*- coding: utf-8 -*-

from DisplayCAL import RealDisplaySizeMM
from DisplayCAL.dev.mocks import check_call, check_call_str
from tests.data.display_data import DisplayData


def test_get_default_size_1():
    """Testing wxMeasureFrame.get_default_size() function."""
    from DisplayCAL.wxMeasureFrame import get_default_size
    import wx

    app = wx.GetApp()
    if not app:
        app = wx.PySimpleApp()
    with check_call_str("DisplayCAL.wxMeasureFrame.getcfg", DisplayData.CFG_DATA):
        with check_call(
            RealDisplaySizeMM, "_enumerate_displays", DisplayData.enumerate_displays()
        ):
            result = get_default_size()
    assert isinstance(result, int)
    assert result > 1
