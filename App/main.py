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
# app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI # pass to where the database is
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

engine = create_engine(DB_URI, echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()
# db = SQLAlchemy(app)

# define the database model
class City(Base):
    __tablename__= "cities"
    id = Column(Integer, primary_key= True)
    name = Column(String(80), unique = True)
    lon = Column(Float)
    lat = Column(Float)
    geo = Column(Geometry("Point"))

    def __init__(self,name, lon, lat, geo):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.geo = geo


    def __repr__(self):
           return "<City {id} {name} ({lat}, {lon})>".format(
               id=self.id, name=self.name, lat=self.lat, lon=self.lon)

    @staticmethod
    def get_cities_within_buffer(cityID, radius):
        city = session.query(City).get(cityID)
        selected_cities = session.query(City).filter(func.ST_DistanceSphere(City.geo, city.geo)< radius).all()
        return selected_cities
    @staticmethod
    def get_distance(cityID1, cityID2):
        city1= session.query(City).get(cityID1)
        city2= session.query(City).get(cityID2)
        distance = session.scalar(func.ST_DistanceSphere(city1.geo, city2.geo))
        return str(distance) + "m"

    @classmethod
    def add_city(cls, name, lon, lat):
        """Put a new city in the database."""
        geo = 'POINT({} {})'.format(lon, lat)
        city = City(name=name, lon=lon, lat=lat, geo=geo)
        session.add(city)
        session.commit()

    @classmethod
    def update_geometries(cls):
        """Using each city's longitude and latitude, add geometry data to db."""
        cities = session.query(City).all()

        for city in cities:
            point = 'ST_POINT({} {})'.format(city.lon, city.lat)
            city.geo = point
        session.commit()

    @staticmethod
    def getSRID(id):
        city = session.query(City).get(id)
        print(1)
        srid = session.scalar(func.ST_SRID(city.geo))
        return srid




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map():
    all_cities = session.query(City).order_by(City.name).all()
    collection = []
    for city in all_cities:
        # convert string to dictionary (for js to read as json)--> use json.loads
        collection.append(json.loads(session.scalar(func.ST_AsGeoJSON(city.geo))))
    return render_template("map.html", cities = collection)

@app.route("/cities")
def cities():
    all_cities = session.query(City).order_by(City.name).all()
    return render_template("cities.html", cities = all_cities)

@app.route("/cities/delete/<int:id>")
def delete(id):
    deleted_city = City.__table__.delete().where(City.id == id)
    session.execute(deleted_city)
    session.commit()
    return redirect("/cities")

@app.route("/cities/edit/<int:id>", methods = ["GET", "POST"])
def edit(id):
    city = session.query(City).get(id)
    if request.method == "POST":
        # to access form data (data transmitted in a POST or PUT request)
        # we can use the form attribute
        city.lon = request.form["longi"]
        city.lat = request.form["lati"]
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
            session.rollback()
        return redirect("/cities")
    else:
        return render_template("new_city.html")

# if we run this directly from the command line
if __name__=="__main__":
    # we turn on the debug mode
    app.run(debug=True)