#!/usr/bin/env python3

import json
import pytest
from amberelectric import AmberElectric

def test_getpricesv2_input_checking():
    """ test a basic thing """
    testapi = AmberElectric()
    with pytest.raises(ValueError) as err_msg:
        testapi.getpricelistv2()

def test_valid_input():
    testapi = AmberElectric()
    #print(testapi.getpricelistv2(postcode='4000'))
    testdata = testapi.getpricelistv2(postcode=4000)
    #print(testdata.keys())
    #print(testdata.get('data').get('networkProvider'))
    print(json.dumps(testdata, indent=2))
    assert True
