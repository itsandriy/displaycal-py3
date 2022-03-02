# -*- coding: utf-8 -*-

from DisplayCAL.util_str import asciize, safe_basestring, safe_str


def test_asciize_working_properly():
    """testing if the ``asciize`` function is working properly"""
    from DisplayCAL.ICCProfile import TextDescriptionType

    tag_data = b"\0" * 8 + b"\x00\x00\x00\x04" + b"test" + b"\0" * 12
    description_type = TextDescriptionType(tagData=tag_data, tagSignature="desc")
    description = str(description_type)
    result = asciize(description)
    expected_result = b"test"
    assert result == expected_result


def test_safe_basestring_1():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError("test the Environment is not being correct")
    assert safe_basestring(env_error) == "test the Environment is not being correct"


def test_safe_basestring_2():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError()
    env_error.reason = "test the Environment is not being correct"
    assert safe_basestring(env_error) == "test the Environment is not being correct"


def test_safe_basestring_3():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError()
    env_error.reason = b"test the Environment is not being correct"
    assert safe_basestring(env_error) == "test the Environment is not being correct"


def test_safe_basestring_4():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError()
    env_error.reason = ["test the Environment is not being correct"]
    assert safe_basestring(env_error) == "test the Environment is not being correct"


def test_safe_basestring_5():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError()
    env_error.reason = [b"test the Environment is not being correct"]
    assert safe_basestring(env_error) == "test the Environment is not being correct"


def test_safe_basestring_6():
    """testing if safe_basestring() is working properly"""
    env_error = EnvironmentError()
    env_error.reason = [123]
    assert safe_basestring(env_error) == "123"


def test_safe_basestring_7():
    """testing if safe_basestring() is working properly"""

    class TestObj(object):
        def __init__(self):
            self.filename = "TestValue.ti3"

    env_error = EnvironmentError()
    test_obj = TestObj()
    env_error.reason = [test_obj]
    assert safe_basestring(env_error) == test_obj.__repr__()


def test_safe_basestring_8():
    """testing if safe_basestring() is working properly"""
    key_error = KeyError("test some key values not being correct")
    assert (
        safe_basestring(key_error)
        == "Key does not exist: 'test some key values not being correct'"
    )


def test_safe_string_1():
    """testing if safe_string() is working properly"""
    obj = "Test value"
    assert safe_str(obj) == "Test value"


def test_safe_string_2():
    """testing if safe_string() is working properly"""
    obj = b"Test value"
    assert safe_str(obj) == "Test value"
