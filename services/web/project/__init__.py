import json


from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, exc
from geoalchemy2 import Geometry


app = Flask(__name__)

app.config.from_object("project.config.Config")
## DB_URI= 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="abc",url="postgis:5432",db="postgres")
# app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI # pass to where the database is
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# define the database model
class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), unique=True)
    lon = db.Column(Float)
    lat = db.Column(Float)
    geo = db.Column(Geometry("Point"))

    def __init__(self, name, lon, lat, geo):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.geo = geo

    def __repr__(self):
        return "<City {id} {name} ({lon}, {lat})>".format(id=self.id, name=self.name, lon=self.lon, lat=self.lat)

    @staticmethod
    def get_cities_within_buffer(city_id, radius):
        city = City.query.filter_by(id=city_id).first()
        coordinate = [city.lat, city.lon]
        selected_cities = City.query.filter((func.ST_DistanceSphere(City.geo, city.geo) < radius), (City.id != city.id)).all()
        return selected_cities, coordinate

    @staticmethod
    def get_distance(city_id_1, city_id_2):
        city1 = City.query.get(city_id_1)
        city2 = City.query.get(city_id_2)
        distance = db.session.scalar(func.ST_DistanceSphere(city1.geo, city2.geo))
        return str(distance) + "m"

    @classmethod
    def add_city(cls, name, lon, lat):
        """Put a new city in the database."""
        geo = 'POINT({} {})'.format(lon, lat)
        city = City(name=name, lon=lon, lat=lat, geo=geo)
        db.session.add(city)
        db.session.commit()

    @staticmethod
    def getSRID(id):
        city = City.query.get(id)
        print(1)
        srid = db.session.scalar(func.ST_SRID(city.geo))
        return srid

    @staticmethod
    def toJSON(city_collection):
        collection = []
        for city in city_collection:
            # convert string to dictionary (for js to read as json)--> use json.loads
            geojson_feature = json.loads(db.session.scalar(func.ST_AsGeoJSON(city.geo)))
            geojson_feature["id"] = city.id
            geojson_feature["properties"] = {"name": city.name}
            collection.append(geojson_feature)
        return collection


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/_getCities")
def get_cities():
    all_cities = City.query.order_by(City.name).all()
    return {"cities": City.toJSON(all_cities)}
#     return jsonify(all_cities)


@app.route("/cities")
def cities():
    try:
        all_cities = City.query.order_by(City.name).all()
    except exc.ProgrammingError:
        return "No table yet"
    return render_template("cities.html", cities=all_cities)


@app.route("/cities/delete/<int:id>")
def delete(id):
    deleted_city = City.__table__.delete().where(City.id == id)
    db.session.execute(deleted_city)
    db.session.commit()
    return redirect(url_for("cities", _external=True))


@app.route("/cities/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    city = City.query.get(id)
    if request.method == "POST":
        # to access form data (data transmitted in a POST or PUT request)
        # we can use the form attribute
        city.lon = request.form["longi"]
        city.lat = request.form["lati"]
        # update the point according to the longitude and latitude
        point = 'POINT({} {})'.format(city.lon, city.lat)
        city.geo = point
        db.session.commit()
        return redirect(url_for("cities", _external=True))
    else:
        return render_template("edit.html", city=city)


@app.route("/cities/new", methods=["GET", "POST"])
def add_new_city():
    if request.method == "POST":
        city_name = request.form["name"]
        city_lon = request.form["longi"]
        city_lat = request.form["lati"]
        try:
            City.add_city(city_name, city_lon, city_lat)
        except exc.IntegrityError:
            db.session.rollback()
        return redirect(url_for("cities", _external=True))
    else:
        return render_template("new_city.html")


# @app.route("/_withinBuffer/<int:id>/<int:distance>")
# def within_buffer(id, distance):
#     cities_in_buffer, city_coord = City.get_cities_within_buffer(id, distance)
#     collection = ""
#     for city in cities_in_buffer:
#         collection += (str(city.name) + " ")
#     if collection != "":
#         return collection + "**" + City.toJSON(cities_in_buffer) + "**[{lat}, {lon}]".format(lat=city_coord[0], lon=city_coord[1])
#     else:
#         return "No spots found."


@app.route("/_searchInBuffer", methods=["GET","POST"])
def search_in_buffer():
    if request.method == "POST":
        id=request.form["t_id"]
        distance=request.form["search_distance"]
        cities_in_buffer, city_coord = City.get_cities_within_buffer(id, distance)
        collection = []
        for city in cities_in_buffer:
            collection.append(city.name)
        if collection != "":
            return {"collection": collection, "cities": City.toJSON(cities_in_buffer), "target_coordinate": "[{lat}, {lon}]".format(lat=city_coord[0], lon=city_coord[1])}
        else:
            return ""




# if we run this directly from the command line
if __name__ == "__main__":
    # we turn on the debug mode
    app.run(debug=True)
