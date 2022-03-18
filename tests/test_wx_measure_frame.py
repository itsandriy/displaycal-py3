# -*- coding: utf-8 -*-

from DisplayCAL import RealDisplaySizeMM
from DisplayCAL.dev.mocks import check_call, check_call_str
from tests.data.display_data import DisplayData

# todo: deactivated test temporary because of pipeline issue
#  INTERNALERROR>   File "/opt/hostedtoolcache/Python/3.8.12/x64/lib/python3.8/posixpath.py", line 379, in abspath
#  NTERNALERROR>     cwd = os.getcwd()
#  INTERNALERROR> FileNotFoundError: [Errno 2] No such file or directorys

# def test_get_default_size_1():
#     """Testing wxMeasureFrame.get_default_size() function."""
#     from DisplayCAL.wxMeasureFrame import get_default_size
#     import wx
#
#     app = wx.GetApp()
#     if not app:
#         app = wx.PySimpleApp()
#     with check_call_str("DisplayCAL.wxMeasureFrame.getcfg", DisplayData.CFG_DATA):
#         with check_call(
#             RealDisplaySizeMM, "_enumerate_displays", DisplayData.enumerate_displays()
#         ):
#             result = get_default_size()
#     assert isinstance(result, int)
#     assert result > 1
