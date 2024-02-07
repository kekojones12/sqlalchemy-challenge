# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect
import json




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


session = Session(engine)
results_measurements = session.query(measurement).all()
results_stations = session.query(station).all() 


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
app = Flask(__name__)
@app.route("/")
def home():
    """List all available api routes."""
    return (f"Available Routes: <br/>"
            f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/<start> <br/>"
            f"/api/v1.0/<start>/<end>")

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2016-08-23').all()
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station, station.name).all()
    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)
    return jsonify(all_stations)

#Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date > '2016-08-23').filter(measurement.station == 'USC00519281').all()
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    all_start = []
    for min, avg, max in results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["avg"] = avg
        start_dict["max"] = max
        all_start.append(start_dict)
    return jsonify(all_start)

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    all_start_end = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["avg"] = avg
        start_end_dict["max"] = max
        all_start_end.append(start_end_dict)
    return jsonify(all_start_end)

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
if __name__ == '__main__':
    app.run(debug=True)
    