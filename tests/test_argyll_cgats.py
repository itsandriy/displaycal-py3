# -*- coding: utf-8 -*-
from DisplayCAL.argyll_cgats import quote_nonoption_args


def test_quote_nonoption_args_1():
    """Testing if the quote_nonoption_args() function is working properly."""
    test_value = [
        "/home/erkan.yilmaz/Downloads/Argyll_V2.3.0/bin/dispread",
        "-v",
        "-d1",
        "-c1",
        "-yn",
        "-P0.4711274060494959,1,1.0",
        "-k",
        "'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX.cal'",
        "'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX'",
    ]

    expected_result = [
        b'"/home/erkan.yilmaz/Downloads/Argyll_V2.3.0/bin/dispread"',
        b'-v',
        b'-d1',
        b'-c1',
        b'-yn',
        b'-P0.4711274060494959,1,1.0',
        b'-k',
        b'"\'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX.cal\'"',
        b'"\'Monitor 1 #1 2022-03-02 23-45 D6500 2.2 F-S XYZLUT+MTX\'"'
     ]

    result = quote_nonoption_args(test_value)
    assert result == expected_result
