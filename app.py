import os
from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from flask_cors import CORS
from models import db, Contact

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["DEBUG"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# production mysql

app.config["ENV"] = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:occam463871@localhost/testapi"


# development sqlite
"""
app.config["ENV"] = "development"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(BASE_DIR, "db.sqlite3")
"""
db.init_app(app)

Migrate(app, db)
CORS(app)

manager = Manager(app)
manager.add_command("db", MigrateCommand)  # init,migrate,upgrade


# GET WITHOUT METHOD SHOULD RETURN EVERY ELEMENT
@app.route("/", methods=("GET", "PUT", "POST", "DELETE"))
def root():
    return render_template("index.html")


@app.route("/api/test", methods=("GET", "POST"))
# THIS METHODS SHOULD USE PARAMETERS TO MODIFY, PUT, DELETE
@app.route("/api/test/<int:id>", methods=["GET", "PUT", "DELETE"])
def test(id=None):
    if request.method == "GET":
        return jsonify({"msg": "method = GET"}), 200
    if request.method == "POST":
        return jsonify({"msg": "method = POST"}), 200
    if request.method == "PUT":
        return jsonify({"msg": "method = PUT"}), 200
    if request.method == "DELETE":
        return jsonify({"msg": "method = DELETE"}), 200


@app.route("/api/contacts", methods=["GET", "POST"])
@app.route("/api/contacts7<int:id>", methods=["GET", "PUT", "DELETE"])
def contacts(id=None):
    if request.method == "GET":
        if id is not None:
            pass
        else:
            # busca la tabla contact y trae todo ("SELECT * FROM contact")
            contacts = Contact.query.all()
            # sobreescribe el array contacts
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            # con un array de diccionarios obtenido desde la funcion serialize
            #  (de contact, creada en model.py)
            return jsonify(contacts), 200

    if request.method == "POST":
        pass
    if request.method == "PUT":
        pass
    if request.method == "DELETE":
        pass


if __name__ == "__main__":
    manager.run()
