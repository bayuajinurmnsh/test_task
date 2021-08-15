import logging
from flask import Flask, Blueprint, request, jsonify, render_template
import requests
import technical


app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

distance_blueprint = Blueprint('blueprint', __name__)

# Separate url for yandex API to 4 config variable
# and set value of each config to specific CONSTANT
# it will make easy if someday we must to change API key
app.config['yandex_api'] = "https://geocode-maps.yandex.ru/1.x/?"
app.config['yandex_key'] = "apikey=7dbd4a65-26ab-4c51-a336-aa4e4c384458"
app.config['yandex_format'] = "&format=json&lang=en_US&sco=latlong&"
app.config['yandex_geocode'] = "geocode="
URL = app.config['yandex_api']
API_KEY = app.config['yandex_key']
FORMAT = app.config['yandex_format']
GEOCODE = app.config['yandex_geocode']


@distance_blueprint.route('/test_task/api/distance_address',
                          methods=['POST'])
def distance_address():
    """
    This function is use for calculating the distance between points
    and seeing whether the destination point is inside or outside
    the MKAD (Moscow ring road)
    """
    if not request.is_json:
        msg = "You have to send data in json format"
        app.logger.info(msg)
        return jsonify({"message": msg}), 415

    json_data = request.get_json()
    if 'address' not in json_data or len(json_data) >= 2:
        msg = "make sure you have key address in your JSON data"
        app.logger.info(msg)
        return jsonify({"message": msg}), 400

    # Check if address is valid or not
    address = (json_data['address'])
    obj_address = technical.TextPreprocessing(address)
    valid_address = obj_address.check_address()
    if valid_address == "invalid":
        msg = "Invalid address!"
        app.logger.info(msg)
        return jsonify({"message": msg}), 422

    # Request data for specific address from yandex API
    address = str(address).replace(" ", "+")
    geolocation = URL + API_KEY + FORMAT + GEOCODE + address
    response = requests.get(geolocation)

    # check if yandex API gives http response 200 or not
    response_200 = str(response)
    if response_200 != "<Response [200]>":
        msg = "Server do not have access to yandex API"
        app.logger.info(msg)
        return jsonify({"message": msg}), 500

    # Check whether yandex can found the specific address or not
    response_data = response.json()
    empty_response = response_data['response']['GeoObjectCollection'][
                'metaDataProperty']['GeocoderResponseMetaData']['found']
    empty_res = int(empty_response)
    if empty_res == 0:
        msg = "Can not find your address!"
        app.logger.info(msg)
        return jsonify({"message": msg}), 404

    # Get latitude and longitude of the specific address from yandex API
    # Count the distance from MKAD to the specific address 
    # if address is outside MKAD
    address_latlong = response_data['response']['GeoObjectCollection']\
                                   ['featureMember'][0]['GeoObject']\
                                   ['Point']['pos']
    long, lat = address_latlong.split(" ")
    address_lat = float(lat)
    address_long = float(long)
    obj_distance = technical.CheckDistance(address_lat, address_long)
    distance = obj_distance.count_distance()
    if distance == "area inside MKAD":
        app.logger.info("area inside MKAD")
        return jsonify({"message":distance}), 200

    # Get specific address from yandex response, so if client just input
    # lat and long value , client will know the specific address of it
    address_details = response_data['response']['GeoObjectCollection']\
                                   ['featureMember'][0]['GeoObject']\
                                   ['metaDataProperty']\
                                   ['GeocoderMetaData']['AddressDetails']\
                                   ['Country']['AddressLine']
    # write result to app.log file
    app.logger.info("distance from MKAD to %s is %s :", 
                    address_details, distance)

    
    return jsonify({"distance": distance, "destination_address":
                  address_details}), 200


app.register_blueprint(distance_blueprint)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)