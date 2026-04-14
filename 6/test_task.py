import pandas as pd
import os.path
import pytest
import json
from pandas.api.types import is_numeric_dtype

def loadjson(fl):
    with open(fl, 'r') as file:
        a = json.load(file)
    return a


payrun = {
    "name": "Payrun.xlsx",
    "data": None,
    "load": lambda: pd.read_excel(payrun["name"], header=[0,1])
}

gtn = {
    "name": "GTN.xlsx",
    "data": None,
    "load": lambda: pd.read_excel(gtn["name"])
}

mapping = {
    "name": "mapping.json",
    "data": None,
    "load": lambda: loadjson(mapping['name'])
}

files = [payrun, gtn, mapping]

def loadfiles(file):
    try:
        file["data"] = file["load"]()
        return True
    except Exception:           # this is why all the tests are in one file, so you can use the variables
        return False


# ▄██ 
#  ██ 
#  ██ 
    
@pytest.fixture
def test_if_files_exist():
    for file in files:
        assert os.path.isfile(file["name"]), f"file {file["name"]} does not exist or is in wrong format"

def test_if_files_readable(test_if_files_exist):
    for file in files:
        assert loadfiles(file), f"file {file["name"]} exists, but is invalid or corrupted"


# ████▄ 
#  ▄██▀ 
# ███▄▄ 

def test_empty_gtn():
    assert not pd.isna(gtn['data'].loc[0]).all(axis=None), "empty line in GTN between the headers and the data"

# ████▄ 
#  ▄▄██ 
# ▄▄▄█▀ 

    
def test_gtn_headers():         #also catches if any header cells are blank
    assert not any(list(map(lambda a: a.startswith("Unnamed"), (list(gtn['data'].columns))))), "one or more header cells are blank in GTN, check for any gaps, data to the right of the table or if the header is properly located on row 1"


# ██  ██       ███▀▀▀ 
# ▀█████       ▀▀███▄ 
#     ██  ▄    ▄▄▄██▀ 
#        ▀            
        
@pytest.fixture               
def makesets():
    return {        #i love python, this would be much less elegant in other languages
        'gtn': set(gtn['data']['employee_id']),
        'payrun': set(payrun['data'].iloc[0:-1]['Employee ID']['Unnamed: 1_level_1'])      #payrun has double headers and last row is used for subtotals
    }

def test_missing_employees_gtn(makesets):
     assert (makesets['gtn'].difference(makesets['payrun']) == set()), "some employees that are present in GTN are missing in Payrun"

def test_missing_employees_payrun(makesets):
     assert (makesets['payrun'].difference(makesets['gtn']) == set()), "some employees that are present in Payrun are missing in GTN"

# ▄██▀▀▀       ██████ 
# ██▄▄▄          ▄██▀ 
# ▀█▄▄█▀  ▄     ██▀   
#        ▀            
@pytest.fixture    
def getmappings():
    return {k: v['vendor'] for k, v in mapping['data']['mappings'].items()}   

def test_mappings_payrun(getmappings):
    assert (set(getmappings.keys())).difference(set(list(payrun['data'].columns.levels[0]) + list(payrun['data'].columns.levels[1]))) == set(), "one or more mapped pay elements from mappings.json do not exist in Payrun"
                #left in mappings                            bit of hacky way to get column names from a miltilevel i guess

def test_mappings_gtn(getmappings):
    assert (set(getmappings.values())).difference(set(gtn['data'].columns)) == set(), "one or more mapped pay elements from mappings.json do not exist in GTN"
            #left in mappings                   right in gtn

# ▄████▄ 
# ██▄▄██ 
# ▀█▄▄█▀ 

def test_gtn_numerical(getmappings):
    assert all(list(map(is_numeric_dtype, (gtn['data'][list(getmappings.values())].dtypes)))), "non-numeric value found in one or more pay element cells in GTN"
