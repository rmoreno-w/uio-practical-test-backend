import os

from flask import Blueprint, json, jsonify, request

people = Blueprint("people", __name__)

current_folder_path = os.path.realpath(os.path.dirname(__file__))
json_uri = os.path.join(current_folder_path, "people_list.json")

# Lists all of the current users
@people.route("/", methods=["GET"])
def list_users():
    try:
        with open(json_uri, 'r') as json_file:
            json_data = json.load(json_file)
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
    try:
        with open(json_uri, 'r') as json_file:
            json_data = json.load(json_file)
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



# Creating New User
@people.route("/create", methods=["POST"])
def create_user():
    # If the request has data
    new_user_data = request.get_json()

    # Checking if all necessary data was sent
    try:
        name = new_user_data["name"]
        email = new_user_data["email"]
        password = new_user_data["password"]
        year_of_birth = new_user_data["year_of_birth"]
    except:
        return jsonify({"message": "You must include a name, email, password and year of birth"}), 400


    try:    
        with open(json_uri, 'r+') as json_file:
            json_data = json.load(json_file)
            json_data["data"].append({
                "name": name,
                "email": email, 
                "password": password,
                "year_of_birth": year_of_birth
            })
            json_file.seek(0,0)
            json.dump(json_data, json_file, indent=4)

            return jsonify({"message": "User created successfully"}), 200

    except:
        return jsonify({"message": "Could not save the user data, please try again in a few seconds"}), 400




# Modification of a User
@people.route("/edit", methods=["PATCH"])
def modificate_user():
    # If the request has data
    new_user_data = request.get_json()

    try:
        name = new_user_data["name"]
    except:
        name = ''

    try:
        year_of_birth = new_user_data["year_of_birth"]
    except:
        year_of_birth = ''


    try:
        email = new_user_data["email"]
        password = new_user_data["password"]

        with open(json_uri, 'r+') as json_file:
            json_data = json.load(json_file)
        
            # Checking if email and password are correct
            for person in json_data["data"]:
                if person["email"] == email:
                    if person["password"] == password:
                        # Only editing data if it wasnt empty (trying to allow one of these as empty fields)
                        if name:
                            person["name"] = name
                        if year_of_birth:
                            person["year_of_birth"] = year_of_birth
                        
                        if (name or year_of_birth):
                            json_file.seek(0,0)
                            json.dump(json_data, json_file, indent=4)
                            return jsonify({"message": "User edited successfully"}), 200


            # If the for loop is over and the method did not return, user was not found or password did not match
            return jsonify({"message": "User not found or incorrect password"}), 400

    except:
        return jsonify({"message": "You must include at least a valid password and email for an user thats already registered"}), 400