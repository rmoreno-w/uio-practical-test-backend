import math
import os
from datetime import date

from flask import Blueprint, json, jsonify, request

calculate = Blueprint("calculate", __name__)

current_folder = os.path.realpath(os.path.dirname(__file__))
folder_above_path = os.path.abspath(os.path.join(current_folder, os.pardir))

json_uri = os.path.join(folder_above_path, 'people', "people_list.json")

@calculate.route('/<int:year>', methods=['GET'])
def calculate_average_age(year):
    try:
        with open(json_uri, 'r') as json_file:
            json_data = json.load(json_file)
    except:
        json_data = {
            "average_age": "No users in the database yet"
        }
        return jsonify(json_data), 400
    

    if len(json_data["data"]) == 0:
        return jsonify({"average_age": "No users in the database yet"}), 400

    age_list = []
    for person in json_data["data"]:
        today_date = date.today()
        year_of_birth = date(int(person["year_of_birth"]), 1, 1)

        if year == int(person["year_of_birth"]):
            print(person)

            delta = today_date - year_of_birth
            difference_in_years = math.floor(delta.days / 365)
            age_list.append(difference_in_years)

    if len(age_list) != 0:
        average_age = sum(age_list) / len(age_list)
        return jsonify({"average_age": average_age}), 200
    else:
        average_age = 0
        return jsonify({"message": f"There were no users found born in the year of {year}", "average_age": average_age}), 400
