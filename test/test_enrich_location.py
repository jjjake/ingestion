import sys
from server_support import server, H, print_error_log
from amara.thirdparty import json
from dplaingestion.akamod.enrich_location import \
    from_abbrev, get_isostate, create_dictionaries, remove_space_around_semicolons, STATES

    
# BEGIN remove_space_around_semilocons tests
def test_remove_space_around_semicolons():
    INPUT = "California; Texas;New York ;  Minnesota  ; Arkansas ;Hawaii;"
    EXPECTED = "California;Texas;New York;Minnesota;Arkansas;Hawaii;"

    OUTPUT = remove_space_around_semicolons(INPUT)
    assert OUTPUT == EXPECTED

# BEGIN from_abbrev tests
def test_from_abbrev1():
    """
    "Ga." should produce Georgia but "in" should not produce Indiana
    """
    INPUT = "Athens in Ga."
    EXPECTED = ["Georgia"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

def test_from_abbrev2():
    """
    Should return array with complete State name as the only element.
    """
    INPUT = "San Diego, C.A."
    EXPECTED = ["California"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

def test_from_abbrev3():
    """
    Should return array with complete State name as the only element.
    """
    INPUT = "San Diego, (CA)"
    EXPECTED = ["California"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

def test_from_abbrev4():
    """
    Should return array with complete State name as the only element.
    """
    INPUT = "Greenville, (S.C.)."
    EXPECTED = ["South Carolina"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

def test_from_abbrev5():
    """
    Should return array with complete State name as the only element.
    """
    INPUT = "Asheville NC "
    EXPECTED = ["North Carolina"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

def test_from_abbrev6():
    """
    Should return array with complete State names as the elements.
    """
    INPUT = "San Diego (C.A.), Asheville (NC), Brookings S.d., Brooklyn  NY."
    EXPECTED = ["California", "North Carolina", "South Dakota", "New York"] 

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT.sort() == EXPECTED.sort()

def test_from_abbrev7():
    INPUT = "Cambridge, Mass."
    EXPECTED = ["Massachusetts"]

    OUTPUT = from_abbrev(INPUT)
    assert OUTPUT == EXPECTED

# BEGIN get_isostate tests
def test_get_isostate_non_string_param_fail():
    """
    Should return error if non-string passed as parameter"
    """
    pass

def test_get_isostate_mass():
    INPUT = "Cambridge, Mass."
    EXPECTED = ("US-MA", "Massachusetts") 

    OUTPUT = get_isostate(INPUT,abbrev="Yes")
    assert OUTPUT == EXPECTED

def test_get_isostate_string_without_state_names_returns_none():
    """
    Should return (None,None) if string parameter does not contain
    state names/abbreviations.
    """
    INPUT = "Canada, Mexico, U.S.; Antarctica."
    OUTPUT = get_isostate(INPUT)

    assert OUTPUT == (None, None)

def test_get_isostate_string_with_state_names_returns_iso_and_state():
    """
    Should return (iso_string, state_string) where iso_string and state_strin
    are semicolon-separated iso3166-2 values and state names, respectively.
    Should not include South Carolina, but instead empty string, because the
    optional frb_abbrev parameter was not passed.
    """
    INPUT = "California;New Mexico;Arizona;New York;(S.C.)"
    EXPECTED = ("US-CA;US-NM;US-AZ;US-NY;", "California;New Mexico;Arizona;New York;")

    OUTPUT = get_isostate(INPUT)
    assert OUTPUT == EXPECTED

# BEGIN create_dictionaries tests
def test_create_dictionaries_one():
    """
    Should return array with one dictionary as the only element if splitting each spatial field on
    semicolons produces only one string for each spatial field.
    """
    INPUT = [{
        "city": "Asheville",
        "county": "Buncombe",
        "state": "North Carolina;",
        "country": "United States",
        "iso3166-2": "US-NC"
    }]
    EXPECTED = [
        {
            "city": "Asheville",
            "county": "Buncombe",
            "state": "North Carolina",
            "country": "United States",
            "iso3166-2": "US-NC"
        }
    ]

    OUTPUT = create_dictionaries(INPUT) 
    assert OUTPUT == EXPECTED

def test_create_dictionaries_many1():
    """
    Should return array with dictionaries as elements if splitting each spatial field on
    semicolons produces multiple strings in any spatial field.
    """
    INPUT = [{
        "city": "La Jolla;Pasadena",
        "county": "San Diego;Los Angeles;Buncombe",
        "state": "California;North Carolina",
        "country": "United States",
        "iso3166-2": "US-CA;US-NC"
    }]
    EXPECTED = [
        {
            "city": "La Jolla",
            "county": "San Diego",
            "state": "California",
            "country": "United States",
            "iso3166-2": "US-CA"
        },
        {
            "city": "Pasadena",
            "county": "Los Angeles",
            "state": "North Carolina",
            "iso3166-2": "US-NC"
        },
        {
            "county": "Buncombe"
        }
    ]

    OUTPUT = create_dictionaries(INPUT)
    assert OUTPUT == EXPECTED

def test_create_dictionaries_many2():
    """
    Should return array with dictionaries as elements if splitting each spatial field on
    semicolons produces multiple strings in any spatial field.
    """
    INPUT = [{
        "city": "La Jolla;Pasadena",
        "county": "San Diego;Los Angeles;Buncombe",
        "state": "California;North Carolina",
        "country": "United States",
        "iso3166-2": "US-CA;US-NC"
    }]
    EXPECTED = [
        {
            "city": "La Jolla",
            "county": "San Diego",
            "state": "California",
            "country": "United States",
            "iso3166-2": "US-CA"
        },
        {
            "city": "Pasadena",
            "county": "Los Angeles",
            "state": "North Carolina",
            "iso3166-2": "US-NC"
        },
        {
            "county": "Buncombe"
        }
    ]

    OUTPUT = create_dictionaries(INPUT)
    assert OUTPUT == EXPECTED

def test_enrich_location_after_provider_specific_enrich_location4():
    """
    Previous specific-provider location did not set state.
    """
    INPUT = {
        "id": "12345",
        "sourceResource": {"spatial": [
            {
                "city": "Asheville; La Jolla",
                "county": "Buncombe;San Diego",
                "country": "United States"
            }
        ]},
        "creator": "Miguel"
    }
    EXPECTED = {
        "id": "12345",
        "sourceResource": {"spatial": [
            {
                "city": "Asheville",
                "county": "Buncombe",
                "country": "United States",
            },
            {
                "city": "La Jolla",
                "county": "San Diego",
            }
        ]},
        "creator": "Miguel"
    }

    url = server() + "enrich_location"
    resp,content = H.request(url,"POST",body=json.dumps(INPUT))
    assert resp.status == 200
    assert json.loads(content) == EXPECTED


def test_enrich_location_no_provider_specific_enrich_location1():
    """
    No previous provider-specific location enrichment and does not contain states
    or state abbreviations.
    """
    INPUT = {
        "id": "12345",
        "sourceResource": {"spatial": [
            "Asheville",
            "Buncombe",
            "United States"
        ]},
        "creator": "Miguel"
    }
    OUTPUT = {
        "id": "12345",
        "sourceResource": {"spatial": [
            { "name": "Asheville" },
            { "name": "Buncombe" },
            { "name": "United States" }
        ]},
        "creator": "Miguel"
    }

    url = server() + "enrich_location"
    resp,content = H.request(url,"POST",body=json.dumps(INPUT))
    assert resp.status == 200
    assert json.loads(content) == OUTPUT

def test_enrich_location_spatial_string():
    """Should handle spatial as string"""
    INPUT = {
        "sourceResource": {
            "spatial": "42 36. 00. N, 72 23. 55. W"
        }
    }
    EXPECTED = {
        "sourceResource": { "spatial": [
            {"name": "42 36. 00. N, 72 23. 55. W"}
        ]}
    }

    url = server() + "enrich_location"
    resp,content = H.request(url,"POST",body=json.dumps(INPUT))
    assert resp.status == 200
    assert json.loads(content) == EXPECTED


def test_removing_bracket():
    """Should remove bracket from the beginning of the name"""
    INPUT = {
        "id": "12345",
        "sourceResource": {"spatial": [
            "Charleston (S.C.); [Germany; Poland; Israel; New York (N.Y.); Georgia (U.S.)"
        ]},
        "creator": "Miguel"
    }
    EXPECTED = {
        "id": "12345",
        "sourceResource": {"spatial": [
            {
                "name" : "Charleston (S.C.)"
            },
            {
                "name": "Germany"
            },
            {
                "name": "Poland"
            },
            {
                "name": "Israel"
            },
            {
                "name": "New York (N.Y.)"
            },
            {
                "name": "Georgia (U.S.)"
            }
        ]},
        "creator": "Miguel"
    }

    url = server() + "enrich_location"
    resp,content = H.request(url,"POST",body=json.dumps(INPUT))
    assert resp.status == 200
    assert json.loads(content) == EXPECTED

def test_enrich_list_of_dictionaries_and_strings():
    """Should handle list of dictionaries and strings"""
    INPUT = {
        "id": "12345",
        "sourceResource": {"spatial": [
            {
                "country": "United States",
                "county": "Buncombe",
                "state": "North Carolina"
            },
            "Rushmore, Mount",
            "Mount Rushmore National Memorial"
        ]}
    }
    EXPECTED = {
        "id": "12345",
        "sourceResource": {"spatial": [
            {
                "country": "United States",
                "county": "Buncombe",
                "state": "North Carolina"
            },
            {
                "name": "Rushmore, Mount"
            },
            {
                "name": "Mount Rushmore National Memorial"
            }
        ]}
    }

    url = server() + "enrich_location"
    resp,content = H.request(url,"POST",body=json.dumps(INPUT))
    assert resp.status == 200
    assert json.loads(content) == EXPECTED


if __name__ == "__main__":
    raise SystemExit("Use nosetest")
