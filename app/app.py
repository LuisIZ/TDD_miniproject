from flask import Flask, request, jsonify
import requests
from geopy.distance import geodesic

app = Flask(__name__)

def fetch_coordinates(city_name):
    '''
    Function to fetch the coordinates of a given city using the Nominatim OpenStreetMap API.
    
    Parameters:
    city_name (str): The name of the city to find coordinates for.
    
    Returns:
    dict: A dictionary containing the latitude and longitude of the city.
    
    Raises:
    ValueError: If the city is not found or there is an error in the API request.
    '''
    api_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {
        'User-Agent': 'Testing App'
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    
    if not response_data:
        raise ValueError("City not found")
    
    return {
        "latitude": response_data[0]['lat'],
        "longitude": response_data[0]['lon']
    }

@app.route("/get_coordinates/", methods=["GET"])
def get_coordinates():
    '''
    API endpoint to get the coordinates of a given city.
    
    Parameters:
    city_name (str): The name of the city to find coordinates for.
    
    Returns:
    dict: A dictionary containing the latitude and longitude of the city.
    '''
    city_name = request.args.get('city_name')
    try:
        coordinates = fetch_coordinates(city_name)
        return jsonify(coordinates)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

def calculate_distance(lat1, lon1, lat2, lon2):
    '''
    Function to calculate the distance between two geographical points.
    
    Parameters:
    lat1 (float): Latitude of the first point.
    lon1 (float): Longitude of the first point.
    lat2 (float): Latitude of the second point.
    lon2 (float): Longitude of the second point.
    
    Returns:
    dict: A dictionary containing the distance in kilometers.
    '''
    coordinates_point_1 = (lat1, lon1)
    coordinates_point_2 = (lat2, lon2)
    distance_km = geodesic(coordinates_point_1, coordinates_point_2).kilometers
    return {"distance": distance_km}

@app.route("/get_distance/", methods=["GET"])
def get_distance():
    '''
    API endpoint to calculate the distance between two geographical points.
    
    Parameters:
    lat1 (float): Latitude of the first point.
    lon1 (float): Longitude of the first point.
    lat2 (float): Latitude of the second point.
    lon2 (float): Longitude of the second point.
    
    Returns:
    dict: A dictionary containing the distance in kilometers.
    '''
    try:
        lat1 = float(request.args.get('lat1'))
        lon1 = float(request.args.get('lon1'))
        lat2 = float(request.args.get('lat2'))
        lon2 = float(request.args.get('lon2'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing coordinates"}), 400

    distance = calculate_distance(lat1, lon1, lat2, lon2)
    return jsonify(distance)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
