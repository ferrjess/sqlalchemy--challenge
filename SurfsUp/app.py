# Import the dependencies.
import numpy as np
import datetime as dt 

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
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data from the last 12 months"""
    most_recent_date = dt.date(2017,8,23)
    calculated_date = most_recent_date - dt.timedelta(days = 365)

    # Query results
    results = dict(session.query(measurement.date,measurement.prcp).filter(measurement.date>=calculated_date).all())

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query results
    results = dict(session.query(station.station,station.name).all())

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = dt.date(2017,8,23)
    calculated_date = most_recent_date - dt.timedelta(days = 365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data"""
    # Query results
    results = dict(session.query(measurement.date,measurement.tobs).filter_by(station = "USC00519281").filter( measurement.date>=calculated_date).all())

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.date(2010, 1 ,1)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    # Query results
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

         #Convert list of tuples into normal list
    tempurature = {}
    tempurature["TMIN"] = results[0][0]
    tempurature["TAVG"] = results[0][1]
    tempurature["TMAX"] = results[0][2]

    return jsonify(tempurature)

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start = dt.date(2010, 1 ,1)
    end = dt.date(2017, 8 ,23)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    # Query results
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start)\
        .filter(measurement.date <= end).all()


    session.close()

     #Convert list of tuples into normal list
    tempuratures = {}
    tempuratures["TMIN"] = results[0][0]
    tempuratures["TAVG"] = results[0][1]
    tempuratures["TMAX"] = results[0][2]

    return jsonify(tempuratures)

if __name__ == '__main__':
    app.run(debug=True)
