# -*- coding: utf-8 -*-


def test_get_default_size_1():
    """Testing wxMeasureFrame.get_default_size() function."""
    from DisplayCAL.config import initcfg
    from DisplayCAL.wxMeasureFrame import get_default_size
    initcfg()
    import wx
    app = wx.GetApp()
    if not app:
        app = wx.PySimpleApp()
    result = get_default_size()
    assert isinstance(result, int)
    assert result > 1
