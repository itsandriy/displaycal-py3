# -*- coding: utf-8 -*-


import pytest


def test_iccprofile_from_chromaticies():
    """testing if the ICCProfile.from_chromaticies() method is working properly
    """
    xy = [(0.6771560743827527, 0.32205471727089957),
          (0.19945851033134956, 0.7266949701661809),
          (0.1515536624045438, 0.04081563046813107),
          (0.3133857119826585, 0.3283378912104931)]
    desc = b"Monitor 1 #1 2022-02-13 20-53 D6500 2.2 VF-S XYZLUT+MTX"
    copyright = b"No copyright. Created with DisplayCAL 3.8.9.3 and ArgyllCMS 2.3.0"
    display_manufacturer = None
    display_name = b"Monitor 1, Output DP-2"
    cat = "Bradford"

    from DisplayCAL import ICCProfile
    ICCProfile.debug = True
    mtx = ICCProfile.ICCProfile.from_chromaticities(
        xy[0][0], xy[0][1],
        xy[1][0], xy[1][1],
        xy[2][0], xy[2][1],
        xy[3][0], xy[3][1],
        2.2,
        desc,
        copyright,
        display_manufacturer,
        display_name,
        cat=cat
    )

    assert isinstance(mtx, ICCProfile.ICCProfile)


def test_iccprofile_get_info():
    """testing if the ICCProfile.get_info() method is working properly
    """
    xy = [(0.6771560743827527, 0.32205471727089957),
          (0.19945851033134956, 0.7266949701661809),
          (0.1515536624045438, 0.04081563046813107),
          (0.3133857119826585, 0.3283378912104931)]
    desc = b"Monitor 1 #1 2022-02-13 20-53 D6500 2.2 VF-S XYZLUT+MTX"
    copyright = b"No copyright. Created with DisplayCAL 3.8.9.3 and ArgyllCMS 2.3.0"
    display_manufacturer = None
    display_name = b"Monitor 1, Output DP-2"
    cat = "Bradford"

    from DisplayCAL import ICCProfile
    ICCProfile.debug = True
    icc = ICCProfile.ICCProfile.from_chromaticities(
        xy[0][0], xy[0][1],
        xy[1][0], xy[1][1],
        xy[2][0], xy[2][1],
        xy[3][0], xy[3][1],
        2.2,
        desc,
        copyright,
        display_manufacturer,
        display_name,
        cat=cat
    )

    expected_result = [
        ['Size', '0 Bytes (0.00 KiB)'],
        ['Preferred CMM', b'0x6172676C'],
        ['ICC version', '2.2'],
        ['Profile class', b'Display device profile'],
        ['Color model', b'RGB'],
        ['Profile connection space (PCS)', b'XYZ'],
        ['Created', '2022-02-14 02:44:22'],
        ['Platform', b'0x2A6E6978'],
        ['Is embedded', 'No'],
        ['Can be used independently', 'Yes'],
        ['Device', ''],
        ['    Manufacturer', b"0x00000000"],
        ['    Model', b'0x00000000'],
        ['    Media attributes', 'Reflective, Glossy, Positive, Color'],
        ['Default rendering intent', 'Perceptual'],
        ['PCS illuminant XYZ', ' 96.42 100.00  82.49 (xy 0.3457 0.3585, CCT 5000K)'],
        ['Creator', b'0x4443414C'],
        ['Checksum', b"0x02F595E98437CAF1593DB03F9DCD15C9"],
        ['    Checksum OK', 'Yes'],
        ["'desc' (ASCII)",
         "b'Monitor 1 #1 2022-02-13 20-53 D6500 2.2 VF-S XYZLUT+MTX'"],
        ["'cprt'",
         "b'No copyright. Created with DisplayCAL 3.8.9.3 and ArgyllCMS 2.3.0'"],
        ["'dmdd' (ASCII)", "b'Monitor 1, Output DP-2'"],
        ["'wtpt'", ''],
        ["    b'Illuminant-relative' XYZ", ' 95.45 100.00 109.12 (xy 0.3134 0.3283)'],
        ["    b'Illuminant-relative' CCT", '6471K'],
        ['        ΔE 2000 to daylight locus', '1.18'],
        ['        ΔE 2000 to blackbody locus', '3.66'],
        ["'arts'", 'Bradford'],
        ['    Matrix', '0.8951 0.2664 -0.1614'],
        ['        ', '-0.7502 1.7135 0.0367'],
        ['        ', '0.0389 -0.0685 1.0296'],
        ['Chromaticity (illuminant-relative)', ''],
        ["    Channel 1 (b'R') xy", '0.6772 0.3221'],
        ["    Channel 2 (b'G') xy", '0.1995 0.7267'],
        ["    Channel 3 (b'B') xy", '0.1516 0.0408'],
        ["'rXYZ'", ''],
        ['    Illuminant-relative XYZ', ' 57.78  27.48   0.07 (xy 0.6772 0.3221)'],
        ['    PCS-relative XYZ', ' 60.96  28.84  -0.07 (xy 0.6794 0.3214)'],
        ["'rTRC'", 'Gamma 2.2'],
        ["'gXYZ'", ''],
        ['    Illuminant-relative XYZ', ' 18.49  67.35   6.84 (xy 0.1995 0.7267)'],
        ['    PCS-relative XYZ', ' 20.41  67.24   6.00 (xy 0.2180 0.7180)'],
        ["'gTRC'", 'Gamma 2.2'],
        ["'bXYZ'", ''],
        ['    Illuminant-relative XYZ', ' 19.18   5.17 102.21 (xy 0.1516 0.0408)'],
        ['    PCS-relative XYZ', ' 15.05   3.92  76.56 (xy 0.1575 0.0411)'],
        ["'bTRC'", 'Gamma 2.2']]

    assert icc.get_info() == expected_result


def test_iccprofile_from_xyz():
    """testing if ICCProfile.from_xyz() method is working properly
    """

    XYZ = {
        'r': [0.5777977275512667, 0.2747999919455954, 0.0006734086960673902],
        'g': [0.18487094167718518, 0.6735475123298383, 0.06844569117319045],
        'b': [0.19179233077154842, 0.05165249572456644, 1.0220629001307424]
    }
    wXYZ = (0.9544610000000001, 1.0, 1.091182)

    desc = b"Monitor 1 #1 2022-02-13 20-53 D6500 2.2 VF-S XYZLUT+MTX"
    copyright = b"No copyright. Created with DisplayCAL 3.8.9.3 and ArgyllCMS 2.3.0"
    display_manufacturer = None
    display_name = b"Monitor 1, Output DP-2"
    cat = "Bradford"

    from DisplayCAL import ICCProfile
    ICCProfile.debug = True
    mtx = ICCProfile.ICCProfile.from_XYZ(
        XYZ["r"], XYZ["g"], XYZ["b"], wXYZ,
        2.2,
        desc,
        copyright,
        display_manufacturer,
        display_name,
        cat=cat
    )

    assert isinstance(mtx, ICCProfile.ICCProfile)


def test_uInt32Number_tohex_is_working_properly():
    """testing if uInt32Number_tohex is working properly
    """
    from DisplayCAL.ICCProfile import uInt32Number_tohex
    test_value = 132123
    result = uInt32Number_tohex(test_value)
    expected_value = b"\x00\x02\x04\x1b"
    assert result == expected_value


def test_dict_type():
    """testing the DictType
    """
    from DisplayCAL.ICCProfile import DictType
    d = DictType()
    d.update({"CMF_product": "DisplayCAL",
              "CMF_binary": "DisplayCAL",
              "CMF_version": "3.8.9.3"})

    expected = (b'dict\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x10\x00\x00\x00@'
                b'\x00\x00\x00\x16\x00\x00\x00X\x00\x00\x00\x14\x00\x00\x00l\x00\x00\x00\x14'
                b'\x00\x00\x00\x80\x00\x00\x00\x14\x00\x00\x00\x94\x00\x00\x00\x16'
                b'\x00\x00\x00\xac\x00\x00\x00\x0e\x00C\x00M\x00F\x00_\x00p\x00r\x00o\x00d'
                b'\x00u\x00c\x00t\x00\x00\x00D\x00i\x00s\x00p\x00l\x00a\x00y\x00C\x00A\x00L'
                b'\x00C\x00M\x00F\x00_\x00b\x00i\x00n\x00a\x00r\x00y\x00D\x00i\x00s\x00p'
                b'\x00l\x00a\x00y\x00C\x00A\x00L\x00C\x00M\x00F\x00_\x00v\x00e\x00r\x00s'
                b'\x00i\x00o\x00n\x00\x00\x003\x00.\x008\x00.\x009\x00.\x003\x00\x00')

    assert d.tagData == expected
