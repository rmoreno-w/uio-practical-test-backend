import os

from flask import Blueprint, json, jsonify

people = Blueprint("people", __name__)

# Lists all of the current users
@people.route("/", methods=["GET"])
def list_users():
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    json_uri = os.path.join(current_folder_path, "people_list.json")
    
    try:
        with open(json_uri, 'r') as json_file:
            json_data = json.load(json_file)
            print(type(json_data))
    # If the file with the data is not found
    except:
        json_data = {
            "data": []
        }
        return jsonify(json_data), 400
    
    # Removing password field for each person found in order to not send password
    for person in json_data["data"]:
        del person["password"]

    return jsonify(json_data), 200


# Query user by email
@people.route("/<email>", methods=["GET"])
def find_user(email):
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    json_uri = os.path.join(current_folder_path, "people_list.json")
    
    try:
        with open(json_uri, 'r') as json_file:
            json_data = json.load(json_file)
            print(type(json_data))
    # If the file with the data is not found
    except:
        json_data = {
            "data": []
        }
        return jsonify(json_data), 400
    
    # Removing password field for each person found in order to not send password
    for person in json_data["data"]:
        if person["email"] == email:
            del person["password"]
            return jsonify(person), 200
        
    #If the search didnt return any person with that email
    return jsonify({"message": "Could not find an user with the email provided"}), 400




