# -*- coding: utf-8 -*-


def test_asciize_working_properly():
    """testing if the ``asciize`` functino is working properly
    """
    from DisplayCAL.util_str import asciize
    obj = Exception("test")
    result = asciize(obj)
    expected_result = ""
    assert result == expected_result
