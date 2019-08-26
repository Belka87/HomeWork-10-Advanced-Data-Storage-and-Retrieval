import numpy as np 
import pandas as pd
import datetime as dt    
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import flask, jsonify



engine = create_engine("sqlite:///Resoursces,hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.mesaurement
Station = Base.classes.station


session = Session(engine)

# weather app
app = Flask(__name__)


latestDate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())

latestDate = list(np.ravel(latestDate))[0]

latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
latestYear = int(dt.datetime.strftime(latestDate, '%Y'))
latestMonth = int(dt.datetime.strftime(latestDate, '%d'))
latestDay = int(dt.datetime.strftime(latestDate, '%d'))

yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)
yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')



@app.route("/")
def home():
    return(f"Welcome to Surf's UP!: Hawaii Climate API<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"Available Routes: <br/>"
            f"/api/v1.0/stations ~~~~ a list of all weather observations stations <br/>"
            f"/api/v1.0/precipitation ~~ the latest year of precipitation data<br/>"
            f"/api/v1.0/temperature ~~ the latest year of temperature data<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"~~~ datasearch (yyyy-mm-dd)<br/>"
            f"/api/v1.0/datasearch/2015-05-30 ~~~~~~~~~low, high, and average temp for date given in each date after<br/>"
            f"/api/v1.0/datasearch/2015-05-30/2016-01-30 ~~ low, high, and average temp for date given in each date up to  and including end date<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"~ data available from 2010-01-01 to 2017-08-28 ~<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>")


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                        .filter(Measurement.date > yearBefore)
                        .order_by(Measurement.date)
                        .all())


    precipData = []
    for result in results:
        precipDict = {result.date: result.prcp, "Station": result.station}
        precipData.append(precipDict)

    return jsonify(precipData)



@app.route("/api/v1.0/temperature")

def temperature():
    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
                        .filter(Measurement.date > yearBefore)
                        .order_by(Measurement.date)
                        .all())

    tempData = []
    for result in results:
        precipDict = {result.date: result.tobs, "Station": result.station}
        tempData.append(tempDict)

    return jsonify(precipData)

@app.route('/api/v1.0/datasearch/<startDate>')
def start (startDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurment.tobs), fun.max(Measurement.tobs)]

    results = (session.query(*sel)
                        .filter(func.strftime("%Y-%m-%d",Measurment.date) >= startDate)
                        .group_by(Measurement.date)
                        .all)()



    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["Hight Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

if __name__=="__main__":
    app.run(debug=True)








    