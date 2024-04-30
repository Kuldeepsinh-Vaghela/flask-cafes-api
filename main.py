from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

our_api_key = "WhatsUpBaby"

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    rows = db.session.execute(db.select(Cafe)).scalars().all()
    req_rows = random.choice(rows)
    return jsonify(cafe= {
        "name" : req_rows.name,
        "map_url" : req_rows.map_url,
        "img_url" : req_rows.img_url,
        "location" : req_rows.location,
        "seats" : req_rows.seats,
        "has_toilets" : req_rows.has_toilet,
        "has_wifi" : req_rows.has_wifi,
        'has_sockets' : req_rows.has_sockets,
        "can_take_calls" : req_rows.can_take_calls,
        "price" : req_rows.coffee_price,
    }
                   )

@app.route("/all", methods=['GET'])
def get_all_cafes():
    req_rows = db.session.execute(db.select(Cafe)).scalars()
    cafes_list = []
    for row in req_rows:
        dic_cafe = {
            "name" : row.name,
            "map_url" : row.map_url,
            "img_url" : row.img_url,
            "location" : row.location,
            "seats" : row.seats,
            "has_toilets" : row.has_toilet,
            "has_wifi" : row.has_wifi,
            'has_sockets' : row.has_sockets,
            "can_take_calls" : row.can_take_calls,
            "price" : row.coffee_price,
        }
        cafes_list.append(dic_cafe)
    return jsonify(cafes = cafes_list)


@app.route("/search")
def get_cafe_at_location():
    loc_value = request.args.get('loc')
    req_rows = db.session.execute(db.select(Cafe).where(Cafe.location == loc_value)).scalars()
    cafes_list = []
    for row in req_rows:
        dic_cafe = {
            "name" : row.name,
            "map_url" : row.map_url,
            "img_url" : row.img_url,
            "location" : row.location,
            "seats" : row.seats,
            "has_toilets" : row.has_toilet,
            "has_wifi" : row.has_wifi,
            'has_sockets' : row.has_sockets,
            "can_take_calls" : row.can_take_calls,
            "price" : row.coffee_price,
        }
        cafes_list.append(dic_cafe)
    return jsonify(cafes = cafes_list)



@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})




@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_data(cafe_id):
    updated_price = request.args.get('new_price')
    rows = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if rows:
        rows.coffee_price = updated_price
        db.session.commit()
        return jsonify(response={
            "success": "Successfully updated the price."
        }), 200
    else:
        return jsonify(error={
            "Not found": "Sorry a cafe with that id was not found in the database"
        }), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    get_api_key = request.args.get('api-key')
    if get_api_key == our_api_key:
        req_row = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if req_row:
            db.session.delete(req_row)
            db.session.commit()

            return jsonify(response={"success":"Successfully deleted the cafe from the database"}),200
        else:
            return jsonify(response={"Failure":"Cannot find the cafe in the database"}),404
        
    else:
        return jsonify(error={
            "Forbidden": "Sorry but you are not allowed. Make sure you have the correct api_key"
        }), 403
        


# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
