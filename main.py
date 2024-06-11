from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def root():
    data = {
        "message": "Hello World"
    }

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)