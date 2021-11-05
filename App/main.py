from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


from sqlalchemy import func
from geoalchemy2 import Geometry

import json


app = Flask(__name__)

DB_URI= 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="abc",url="postgis:5432",db="postgres")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI # pass to where the database is
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# engine = create_engine(DB_URI, echo = True)
# Base = declarative_base()
# Session = sessionmaker(bind = engine)
# session = Session()
db = SQLAlchemy(app)

# define the database model
class City(db.Model):
    __tablename__= "cities"
    id = db.Column(Integer, primary_key= True)
    name = db.Column(String(80), unique = True)
    lon = db.Column(Float)
    lat = db.Column(Float)
    geo = db.Column(Geometry("Point"))

    def __init__(self,name, lon, lat, geo):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.geo = geo


    def __repr__(self):
           return "<City {id} {name} ({lon}, {lat})>".format(
               id=self.id, name=self.name, lon=self.lon, lat=self.lat,)

    @staticmethod
    def get_cities_within_buffer(cityID, radius):
        city = City.query.get(cityID)
        selected_cities = City.query.filter(func.ST_DistanceSphere(City.geo, city.geo)< radius).all()
        return selected_cities

    @staticmethod
    def get_distance(cityID1, cityID2):
        city1= City.query.get(cityID1)
        city2= City.query.get(cityID2)
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



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map():
    all_cities = City.query.order_by(City.name).all()
    collection = []
    for city in all_cities:
        # convert string to dictionary (for js to read as json)--> use json.loads
        geojsonFeature = json.loads(db.session.scalar(func.ST_AsGeoJSON(city.geo)))
        geojsonFeature["properties"] = {"name": city.name}
        collection.append(geojsonFeature)
    return render_template("map.html", cities = collection)

@app.route("/cities")
def cities():
    all_cities = City.query.order_by(City.name).all()
    return render_template("cities.html", cities = all_cities)

@app.route("/cities/delete/<int:id>")
def delete(id):
    deleted_city = City.__table__.delete().where(City.id == id)
    db.session.execute(deleted_city)
    db.session.commit()
    return redirect("/cities")

@app.route("/cities/edit/<int:id>", methods = ["GET", "POST"])
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
        return redirect("/cities")
    else:
        return render_template("edit.html", city=city)

@app.route("/cities/new", methods = ["GET", "POST"])
def addNew():
    if request.method == "POST":
        city_name = request.form["name"]
        city_lon = request.form["longi"]
        city_lat = request.form["lati"]
        try:
            new_city = City.add_city(city_name, city_lon, city_lat)
        except IntegrityError:
            db.session.rollback()
        return redirect("/cities")
    else:
        return render_template("new_city.html")

# if we run this directly from the command line
if __name__=="__main__":
    # we turn on the debug mode
    app.run(debug=True)