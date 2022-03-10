# -*- coding: utf-8 -*-

from DisplayCAL.ordereddict import OrderedDict


def test_slicing_is_working_1():
    """Testing if slicing is working properly with OrderedDict."""
    a = OrderedDict()
    a.update({
        3: 'a',  # 0
        1: 'b',  # 1
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',   # 4
        123: 'f',   # 5
        55: 'g',   # 6
    })
    assert a[2:5] == {
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',  # 4
    }


def test_slicing_is_working_2():
    """Testing if slicing is working properly with OrderedDict."""
    initial_dict = {
        3: 'a',  # 0
        1: 'b',  # 1
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',  # 4
        123: 'f',  # 5
        55: 'g',  # 6
    }
    a = OrderedDict(initial_dict)
    assert a == initial_dict
    assert a[2:5] == {
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',  # 4
    }


def test_slicing_is_working_3():
    """Testing if slicing is working properly with OrderedDict."""
    a = OrderedDict()
    a.update({
        3: 'a',  # 0
        1: 'b',  # 1
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',   # 4
        123: 'f',   # 5
        55: 'g',   # 6
    })
    assert a[2:] == {
        2: 'c',  # 2
        10: 'd',  # 3
        5: 'e',  # 4
        123: 'f',  # 5
        55: 'g',  # 6
    }
