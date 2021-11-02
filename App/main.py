from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry


app = Flask(__name__)

DB_URI= 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="abc",url="postgis:5432",db="postgres")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI # pass to where the database is
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# define the database model
class City(db.Model):
    __tablename__= "cities"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique = True)
    lon = db.Column(db.Float)
    lat = db.Column(db. Float)
    geo = db.Column(Geometry("Point"))

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
        city = City.query.get(cityID)
        selected_cities = City.query.filter(func.ST_DWithin(City.geo, city.geo, radius)).all()
        return selected_cities

    @classmethod
    def add_city(cls, name, lon, lat):
        """Put a new city in the database."""
        geo = 'POINT({} {})'.format(lon, lat)
        city = City(name=name, lon=lon, lat=lat, geo=geo)
        db.session.add(city)
        db.session.commit()
    @classmethod
    def update_geometries(cls):
        """Using each city's longitude and latitude, add geometry data to db."""
        cities = City.query.all()

        for city in cities:
            point = 'ST_POINT({} {})'.format(city.lon, city.lat)
            func.ST_SetSRID(point, 4326)

        db.session.commit()
    @classmethod
    def setSRID(cls):
        cities = City.query.all()
        for city in cities:
            func.ST_Transform(city.geo,3785)
        db.session.commit()
    @staticmethod
    def getSRID(id):
        city = City.query.get(id)
        print(1)
        srid = func.ST_SRID(city.geo)
        return srid

@app.route("/")
def index():
    all_cities = City.query.order_by(City.name).all()
    return render_template("index.html", cities = all_cities)



# if we run this directly from the command line
if __name__=="__main__":
    # we turn on the debug mode
    app.run(debug=True)