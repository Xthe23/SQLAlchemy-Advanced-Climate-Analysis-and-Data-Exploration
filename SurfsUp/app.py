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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


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
        f"/api/v1.0/start year<br/>"
        f"/api/v1.0/start year/end year<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all precipitation data for the year 2017"""
    # Query precipitation data for the year 2017 and exclude null values
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2017-01-01').\
        filter(Measurement.date <= '2017-12-31').\
        filter(Measurement.prcp.isnot(None)).all()

    session.close()

    # Convert the query results to a dictionary
    all_precipitation = {date: prcp for date, prcp in results}

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    """Return a list of all tobs for the year 2016"""
    # Query all tobs for the year 2016
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-01-01').\
        filter(Measurement.date <= '2016-12-31').\
        filter(Measurement.station == active_stations[0][0]).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    """Return a list of all tobs"""
    # Query all tobs for the previous year
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.station, Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_start = []
    for station, date, min_temp, avg_temp, max_temp in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["station"] = station
        start_dict["min_temp"] = min_temp
        start_dict["avg_temp"] = avg_temp
        start_dict["max_temp"] = max_temp
        all_start.append(start_dict)

    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    """Return a list of all tobs"""
    # Query all tobs for the specified date range
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end + '-12-31').\
        group_by(Measurement.station, Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_end = []
    for station, date, min_temp, avg_temp, max_temp in results:
        start_end_dict = {}
        start_end_dict["station"] = station
        start_end_dict["date"] = date
        start_end_dict["min_temp"] = min_temp
        start_end_dict["avg_temp"] = avg_temp
        start_end_dict["max_temp"] = max_temp
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)


if __name__ == '__main__':
    app.run(debug=True)
