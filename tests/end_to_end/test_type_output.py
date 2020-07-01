import pytest
import json

ROUTE = "/people"  # TODO change?


def run_query(client, key, value, expected_value=None):
    # If no expected_value is provided, assert it returns the given value
    if not expected_value:
        expected_value = value

    post_body = {key: value}
    resp = client.post(ROUTE, json=post_body)
    id_ = resp.json
    id_ = id_["id"]

    resp_data = client.get(f"{ROUTE}/{id_}")
    resp = json.loads(resp_data.data)

    assert resp[key] == expected_value


@pytest.mark.requiresdb
def test_string(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "string", "asdf1234")


@pytest.mark.requiresdb
def test_number(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "number", 1234.0)
    run_query(all_types_generated_e2e_client, "number", 1234, 1234.0)


@pytest.mark.requiresdb
def test_integer(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "integer", 1234)


@pytest.mark.requiresdb
def test_boolean(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "boolean", False)
    run_query(all_types_generated_e2e_client, "boolean", True)


@pytest.mark.requiresdb
def test_object(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "object", {"json": "test"})


@pytest.mark.requiresdb
def test_array(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "array", ["one", "two", "three"])


@pytest.mark.requiresdb
def test_date(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "date", "2012-04-23")


# This will error if you provide a lower resolution of milliseconds.
@pytest.mark.requiresdb
def test_time(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "time", "18:25:43.511122Z")


@pytest.mark.requiresdb
def test_datetime(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "datetime", "2012-04-23T18:25:43Z")


# This will error if you provide a lower resolution of milliseconds.
@pytest.mark.requiresdb
def test_datetime_with_miliseconds(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "datetime", "2012-04-23T18:25:43.511000Z")


@pytest.mark.requiresdb
def test_year(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "year", 2012)


@pytest.mark.requiresdb
def test_yearmonth(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "yearmonth", "2012-11")


@pytest.mark.requiresdb
def test_duration(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "duration", "11")


@pytest.mark.requiresdb
def test_geopoint(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "geopoint", "41.12,-71.34")


@pytest.mark.requiresdb
def test_geojson(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "geopoint", "41.12,-71.34")
    # https://geojson.org/


@pytest.mark.requiresdb
def test_any(all_types_generated_e2e_client):
    run_query(all_types_generated_e2e_client, "any", "asdf1234")
