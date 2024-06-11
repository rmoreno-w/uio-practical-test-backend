from flask import Flask

from people.people import people

app = Flask(__name__)
app.register_blueprint(people, url_prefix='/people')

if __name__ == '__main__':
    app.run(debug=True)