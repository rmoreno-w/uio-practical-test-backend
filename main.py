from flask import Flask
from flask_cors import CORS, cross_origin

from calculate.calculate import calculate
from people.people import people

app = Flask(__name__)
CORS(app)

app.register_blueprint(people, url_prefix='/people')
app.register_blueprint(calculate, url_prefix='/calculate')

if __name__ == '__main__':
    app.run(debug=True)