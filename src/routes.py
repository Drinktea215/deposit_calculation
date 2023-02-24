from flask import Flask, request
from src.calc_func import *

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def start():
    if request.method == "POST":
        try:
            data = request.get_json()
        except Exception:
            return {"error": "No data"}, 400

        errors = check_dict(data)

        try:
            if len(errors) > 0:
                errors = '\n'.join(errors)
                raise KeyError
        except KeyError:
            return {"error": f"No following data:\n{errors}"}, 400

        date, periods, amount, rate = get_data(data)

        try:
            date, periods, amount, rate, errors = check_data(date, periods, amount, rate)
            if len(errors) > 0:
                errors = '\n'.join(errors)
                raise Exception
        except Exception:
            return {"error": f"The following data contains errors:\n{errors}"}, 400

        return calculate_deposit(date, periods, amount, rate), 200

    elif request.method == "GET":
        return {"error": "No data"}, 400
    else:
        return {"error": "Is there something wrong"}, 400
