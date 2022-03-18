# -*- coding: utf-8 -*-

import wx

from DisplayCAL import RealDisplaySizeMM
from DisplayCAL.dev.mocks import check_call, check_call_str
from DisplayCAL.wxMeasureFrame import get_default_size
from tests.data.display_data import DisplayData


def test_get_default_size_1() -> None:
    """Testing wxMeasureFrame.get_default_size() function."""
    with check_call_str("DisplayCAL.wxMeasureFrame.getcfg", DisplayData.CFG_DATA):
        with check_call_str(
            "DisplayCAL.wxMeasureFrame.get_display_number",
            DisplayData.DISPLAY_DATA["screen"],
        ):
            with check_call(wx, "Display", DisplayData()):
                with check_call(
                    RealDisplaySizeMM,
                    "RealDisplaySizeMM",
                    DisplayData.DISPLAY_DATA["size"],
                ):
                    result = get_default_size()
    assert isinstance(result, int)
    assert result > 1
