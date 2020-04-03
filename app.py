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


"""
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
"""


@app.route("/api/contacts", methods=["GET", "POST"])
@app.route("/api/contacts/<int:id>", methods=["GET", "PUT", "DELETE"])
def contacts(id=None):
    if request.method == "GET":
        if id is not None:
            contacts = Contact.query.get(id)
            if contacts:
                return jsonify(contacts.serialize()), 200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else:
            # busca la tabla contact y trae todo ("SELECT * FROM contact")
            contacts = Contact.query.all()
            # sobreescribe el array contacts
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            # con un array de diccionarios obtenido desde la funcion serialize
            #  (de contact, creada en model.py)
            return jsonify(contacts), 200

    if request.method == "POST":
        # revisa la request y captura el elemento name, idem para phone
        name = request.json.get("name", None)
        phone = request.json.get("phone", None)

        if not name or name == "":  # si no llego un nombre o el nombre esta vacio
            return jsonify({"msg": "Field name is required"}), 400  # 422
        if not phone or phone == "":  # si no llego un nombre o el nombre esta vacio
            return jsonify({"msg": "Field phone is required"}), 400  # 422

        # contact= Contact(name=name,phone=phone) option 1
        contact = Contact()
        contact.name = name
        contact.phone = phone
        db.session.add(contact)
        db.session.commit()

        return jsonify(contact.serialize()), 200  # CREATED

    if request.method == "PUT":
        # revisa la request y captura el elemento name, idem para phone
        name = request.json.get("name", None)
        phone = request.json.get("phone", None)

        if not name or name == "":  # si no llego un nombre o el nombre esta vacio
            return jsonify({"msg": "Field name is required"}), 400  # 422
        if not phone or phone == "":  # si no llego un nombre o el nombre esta vacio
            return jsonify({"msg": "Field phone is required"}), 400  # 422

        # contact= Contact(name=name,phone=phone) option 1
        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Not Found"}), 404

        contact.name = name
        contact.phone = phone

        db.session.commit()

        return jsonify(contact.serialize()), 200  # CREATED

    if request.method == "DELETE":
        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Not Found"}), 400

        db.session.delete(contact)
        db.session.commit()
        return jsonify({"msg": "contact was deleted"}), 200


if __name__ == "__main__":
    manager.run()
