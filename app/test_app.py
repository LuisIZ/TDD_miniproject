import pytest
from app import app


# Fixture to create a test client for the Flask app
@pytest.fixture
def client():
    """
    Pytest fixture to set up the test client for the Flask app.

    Yields:
        client: A Flask test client.
    """
    with app.test_client() as client:
        yield client


# Test case to check the successful response of get_coordinates endpoint
def test_get_coordinates_success(client):
    """
    Test case to verify the successful response of the get_coordinates endpoint.

    Args:
        client: The Flask test client.

    Asserts:
        - The response status code is 200 (OK).
        - The response JSON contains 'latitude'.
        - The response JSON contains 'longitude'.
    """
    response = client.get("/get_coordinates/?city_name=Lima, Peru")
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    data = response.get_json()  # Get the response data in JSON format
    assert "latitude" in data  # Check if 'latitude' is in the response data
    assert "longitude" in data  # Check if 'longitude' is in the response data


# Test case to check the failure response of get_coordinates endpoint for an unknown city
def test_get_coordinates_failure(client):
    """
    Test case to verify the failure response of the get_coordinates endpoint for an unknown city.

    Args:
        client: The Flask test client.

    Asserts:
        - The response status code is 404 (Not Found).
    """
    response = client.get("/get_coordinates/?city_name=UnknownCityXYZ")
    assert response.status_code == 404  # Check if the status code is 404 (Not Found)


# Test case to check the successful response of get_distance endpoint
def test_get_distance_success(client):
    """
    Test case to verify the successful response of the get_distance endpoint.

    Args:
        client: The Flask test client.

    Asserts:
        - The response status code is 200 (OK).
        - The response JSON contains 'distance'.
        - The distance value is non-negative.
    """
    response = client.get("/get_distance/?lat1=0&lon1=0&lat2=1&lon2=1")
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    data = response.get_json()  # Get the response data in JSON format
    assert "distance" in data  # Check if 'distance' is in the response data
    assert data["distance"] >= 0  # Check if the distance is non-negative


# Test case to check the failure response of get_distance endpoint with missing parameters
def test_get_distance_failure(client):
    """
    Test case to verify the failure response of the get_distance endpoint when parameters are missing.

    Args:
        client: The Flask test client.

    Asserts:
        - The response status code is 400 (Bad Request).
    """
    response = client.get("/get_distance/?lat1=0&lon1=0")
    assert response.status_code == 400  # Check if the status code is 400 (Bad Request)


# Parameterized test case to check the get_coordinates endpoint for multiple cities
@pytest.mark.parametrize(
    "city_name, expected_lat, expected_lon",
    [
        ("London", 51.5074, -0.1278),
        ("New York", 40.7128, -74.0060),
        ("Paris", 48.8566, 2.3522),
        ("Tokyo", 35.6895, 139.6917),
    ],
)
def test_the_result_is_correct_for_all_inputs_get_coordinates(
    client, city_name, expected_lat, expected_lon
):
    """
    Parameterized test case to verify the get_coordinates endpoint for multiple cities.

    Args:
        client: The Flask test client.
        city_name: The name of the city to get coordinates for.
        expected_lat: The expected latitude of the city.
        expected_lon: The expected longitude of the city.

    Asserts:
        - The response status code is 200 (OK).
        - The latitude value is within 1km tolerance of the expected latitude.
        - The longitude value is within 1km tolerance of the expected longitude.
    """
    response = client.get(f"/get_coordinates/?city_name={city_name}")
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    data = response.get_json()  # Get the response data in JSON format
    assert (
        abs(float(data["latitude"]) - expected_lat) < 1
    )  # Check if the latitude is within 1km tolerance
    assert (
        abs(float(data["longitude"]) - expected_lon) < 1
    )  # Check if the longitude is within 1km tolerance


# Parameterized test case to check the get_distance endpoint for multiple pairs of coordinates
@pytest.mark.parametrize(
    "lat1, lon1, lat2, lon2, expected_distance",
    [
        (51.5074, -0.1278, 48.8566, 2.3522, 343.56),  # London to Paris
        (40.7128, -74.0060, 34.0522, -118.2437, 3940),  # New York to Los Angeles
        (35.6895, 139.6917, 37.7749, -122.4194, 8289),  # Tokyo to San Francisco
        (52.5200, 13.4050, 41.9028, 12.4964, 1184),  # Berlin to Rome
    ],
)
def test_the_result_is_correct_for_all_inputs_get_distance(
    client, lat1, lon1, lat2, lon2, expected_distance
):
    """
    Parameterized test case to verify the get_distance endpoint for multiple pairs of coordinates.

    Args:
        client: The Flask test client.
        lat1: The latitude of the first point.
        lon1: The longitude of the first point.
        lat2: The latitude of the second point.
        lon2: The longitude of the second point.
        expected_distance: The expected distance between the two points.

    Asserts:
        - The response status code is 200 (OK).
        - The distance value is within 5km tolerance of the expected distance.
    """
    response = client.get(
        f"/get_distance/?lat1={lat1}&lon1={lon1}&lat2={lat2}&lon2={lon2}"
    )
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    data = response.get_json()  # Get the response data in JSON format
    assert (
        abs(data["distance"] - expected_distance) < 5
    )  # Check if the distance is within 5km tolerance
