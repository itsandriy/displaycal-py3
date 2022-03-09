# -*- coding: utf-8 -*-

from DisplayCAL.worker import make_argyll_compatible_path, Worker


# todo: deactivated test temporarily
# def test_get_options_from_profile_is_working_properly(data_files):
#     """testing if ``DisplayCAL.worker.get_options_from_profile()`` is working properly
#     """
#     from DisplayCAL.worker import get_options_from_profile
#     options = get_options_from_profile(profile=data_files["default.ti3"].absolute())


def test_make_argyll_compatible_path_1():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = "C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = 'C_Program Files_some path_excutable.exe'
    assert result == expected_result


def test_make_argyll_compatible_path_2():
    """testing if make_argyll_compatible_path is working properly with bytes input"""
    test_value = b"C:\\Program Files\\some path\\excutable.exe"
    result = make_argyll_compatible_path(test_value)
    expected_result = b'C_Program Files_some path_excutable.exe'
    assert result == expected_result


def test_worker_get_instrument_name_1():
    """testing if the Worker.get_instrument_name() is working properly"""
    worker = Worker()
    result = worker.get_instrument_name()
    expected_result = ""
    assert result == expected_result


def test_worker_get_instrument_features():
    """testing if Worker.get_instrument_features() is working properly"""
    worker = Worker()
    result = worker.get_instrument_features()
    assert result == {}


def test_worker_instrument_supports_css_1():
    """testing if Worker.instrument_supports_ccss is working properly"""
    worker = Worker()
    result = worker.instrument_supports_ccss()
    expected_result = None
    assert result == expected_result


def test_generate_b2a_from_inverse_table(data_files):
    """Test Worker.generate_B2A_from_inverse_table() method"""
    worker = Worker()
    from DisplayCAL import ICCProfile
    icc_profile1 = ICCProfile.ICCProfile(profile=data_files["default.icc"].absolute())

    XYZ = {
        "r": [0.5777977275512667, 0.2747999919455954, 0.0006734086960673902],
        "g": [0.18487094167718518, 0.6735475123298383, 0.06844569117319045],
        "b": [0.19179233077154842, 0.05165249572456644, 1.0220629001307424],
    }
    wXYZ = (0.9544610000000001, 1.0, 1.091182)

    desc = b"Monitor 1 #1 2022-02-13 20-53 D6500 2.2 VF-S XYZLUT+MTX"
    copyright = b"No copyright. Created with DisplayCAL 3.8.9.3 and ArgyllCMS 2.3.0"
    display_manufacturer = None
    display_name = b"Monitor 1, Output DP-2"
    cat = "Bradford"

    from DisplayCAL import ICCProfile

    ICCProfile.debug = True
    icc_profile2 = ICCProfile.ICCProfile.from_XYZ(
        XYZ["r"],
        XYZ["g"],
        XYZ["b"],
        wXYZ,
        2.2,
        desc,
        copyright,
        display_manufacturer,
        display_name,
        cat=cat,
    )

    inverse_table = worker.generate_B2A_from_inverse_table(icc_profile2)
    assert inverse_table is not None
