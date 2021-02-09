# import Flask
from flask import Flask, jsonify

# import SQLAlchemy  
import sqlalchemy
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt 

# import Pandas
import numpy as np
import pandas as pd 

# database setup 
engine = create_engine('sqlite:///hawaii.sqlite')

# reflect existing database into a new model
Base = automap_base()

# reflect the tables 
Base.prepare(engine, reflect=True)

# save reference to the table 
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session 
session = Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

## Flask Routes ##
@app.route("/")
def home():
    return (
        f"Welcome to Temperature Site<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    one_year_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
    prcp_dict = {date: prcp for date, prcp in one_year_data}
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list=stations_list)



@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    active_station_year = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous_year).all()
    tobs_list = list(np.ravel(active_station_year))

    return jsonify(tobs_list=tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    stats_list = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end: 
        start_range_output = session.query(stats_list).filter(Measurement.date >= start).all()
        start_range_list = list(np.ravel(start_range_output))

        return jsonify(start_range_list)
    start_end_range_output = session.query(stats_list).\
    filter(Measurement.date >= start).\
    filter(Measurement.date<= end).all()
    start_end_list = list(np.ravel(start_end_range_output))

    return jsonify(start_end_list)  

if __name__ == "__main__":
    app.run(debug=True)