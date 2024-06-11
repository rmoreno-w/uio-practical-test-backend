import os

from flask import Blueprint, json, jsonify

people = Blueprint("people", __name__)

# Lists all of the current users
@people.route("/", methods=["GET"])
def people_home():
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    json_uri = os.path.join(current_folder_path, "people_list.json")
    
    with open(json_uri, 'r') as json_file:
        json_data = json.load(json_file)
        print(type(json_data))
    
    # Removing password field for each person found in order to not send password
    for person in json_data["data"]:
        del person["password"]

    return jsonify(json_data), 200