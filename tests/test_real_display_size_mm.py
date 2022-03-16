# -*- coding: utf-8 -*-

#from DisplayCAL import config
#from DisplayCAL import RealDisplaySizeMM

# todo: temporarily disabled because test tries to access temporary directory
#  which is no longer present (or never created) with github actions
# def test_real_display_size_mm():
#     """Test DisplayCAL.RealDisplaySizeMM.RealDisplaySizeMM() function."""
#     config.initcfg()
#     display_size = RealDisplaySizeMM.RealDisplaySizeMM(0)
#     assert display_size != (0, 0)
#     assert display_size[0] > 1
#     assert display_size[1] > 1
#
#
# def test_xrandr_output_x_id_1():
#     """Test DisplayCAL.RealDisplaySizeMM.GetXRandROutputXID() function."""
#     config.initcfg()
#     result = RealDisplaySizeMM.GetXRandROutputXID(0)
#     assert result != 0
#
#
# def test_enumerate_displays():
#     """Test DisplayCAL.RealDisplaySizeMM.enumerate_displays() function."""
#     RealDisplaySizeMM._displays = None
#     assert RealDisplaySizeMM._displays is None
#     result = RealDisplaySizeMM.enumerate_displays()
#     assert result[0]['description'] != ''
#     assert result[0]['edid'] != ''
#     assert result[0]['icc_profile_atom_id'] != ''
#     assert result[0]['icc_profile_output_atom_id'] != ''
#     assert result[0]['name'] != ''
#     assert result[0]['output'] != ''
#     assert result[0]['pos'] != ''
#     assert result[0]['ramdac_screen'] != ''
#     assert result[0]['screen'] != ''
#     assert result[0]['size'] != ''
#     assert isinstance(result[0]['size'][0], int)
#     assert isinstance(result[0]['size'][1], int)
#     assert result[0]['size_mm'] != ''
#     assert isinstance(result[0]['size_mm'][0], int)
#     assert isinstance(result[0]['size_mm'][1], int)
#     assert result[0]['x11_screen'] != ''
#     assert result[0]['xrandr_name'] != ''
#     assert RealDisplaySizeMM._displays is not None
#
#
# def test_get_display():
#     """Test DisplayCAL.RealDisplaySizeMM.get_display() function."""
#     config.initcfg()
#     RealDisplaySizeMM._displays = None
#     assert RealDisplaySizeMM._displays is None
#     display = RealDisplaySizeMM.get_display()
#     assert RealDisplaySizeMM._displays is not None
#     assert isinstance(display, dict)
#
#
# def test_get_x_display():
#     """Test DisplayCAL.RealDisplaySizeMM.get_x_display() function."""
#     config.initcfg()
#     display = RealDisplaySizeMM.get_x_display(0)
#     assert isinstance(display, tuple)
#     assert len(display) == 3
#
#
# def test_get_x_icc_profile_atom_id():
#     """Test DisplayCAL.RealDisplaySizeMM.get_x_icc_profile_atom_id() function."""
#     config.initcfg()
#     result = RealDisplaySizeMM.get_x_icc_profile_atom_id(0)
#     assert result is not None
#     assert isinstance(result, int)
#
#
# def test_get_x_icc_profile_output_atom_id():
#     """Test DisplayCAL.RealDisplaySizeMM.get_x_icc_profile_atom_id() function."""
#     config.initcfg()
#     result = RealDisplaySizeMM.get_x_icc_profile_atom_id(0)
#     assert result is not None
#     assert isinstance(result, int)
