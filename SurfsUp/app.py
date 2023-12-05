# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
stations = Base.classes.station
measurements = Base.classes.measurement

# Create our session (link) from Python to the DB <-- I will do this within the routes themselves.
# session = Session(engine)
# conn = engine.connect()


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(measurements.date, measurements.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    results = session.query(stations.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_stations = session.query(measurements.station, func.count(measurements.station)).\
        group_by(measurements.station).\
        order_by(func.count(measurements.station).desc()).all()

    """Return a list of all tobs"""
    # Query all tobs for the previous year
    results = session.query(measurements.date, measurements.tobs).\
        filter(measurements.date >= '2016-08-23').\
        filter(measurements.station == active_stations[0][0]).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    """Return a list of all tobs"""
    # Query all tobs for the previous year
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_start = list(np.ravel(results))

    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    """Return a list of all tobs"""
    # Query all tobs for the previous year
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start).\
        filter(measurements.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_end = list(np.ravel(results))

    return jsonify(all_start_end)
