from flask import Flask

from calculate.calculate import calculate
from people.people import people

app = Flask(__name__)
app.register_blueprint(people, url_prefix='/people')
app.register_blueprint(calculate, url_prefix='/calculate')

if __name__ == '__main__':
    app.run(debug=True)