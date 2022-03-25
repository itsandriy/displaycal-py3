# -*- coding: utf-8 -*-

import wx
from DisplayCAL import display_cal
from DisplayCAL.worker import Worker


def test_update_colorimeter_correction_matrix_ctrl_items_1():
    """testing the MainFrame.update_colorimeter_correction_matrix_ctrl_items() method"""
    # I have no idea how it works, let's see...
    app = wx.GetApp()
    if not app:
        app = wx.App()
    worker = Worker()
    mf = display_cal.MainFrame(worker=worker)
    assert mf.colorimeter_correction_matrix_ctrl.Items != []
    before_items = mf.colorimeter_correction_matrix_ctrl.Items
    before_length = len(before_items)
    mf.update_colorimeter_correction_matrix_ctrl_items()
    after_items = mf.colorimeter_correction_matrix_ctrl.Items
    after_length = len(after_items)
    assert before_length == after_length
    assert before_items == after_items  # Really don't know anything about the method
    # but it was raising errors before, now it is fixed.
