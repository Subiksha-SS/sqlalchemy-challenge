# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func


#################################################
# Database Setup
#################################################

# creating engine to connect to database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base=automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Stations = Base.classes.station




#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Home page Route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather station API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# Route with Precipitation data from a year ago
@app.route("/api/v1.0/precipitation")
def precipitation():
    # date from a year ago
    one_year_ago = '2016-08-23'
    # Create our session (link) from Python to the DB
    session=Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    # Close our session
    session.close()

    # Create a dictionary and append to a list of all_prcp
    all_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)


# Route with all the Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    active_stations = session.query(Stations.station).all()
        # Close our session
    session.close()
    
    # Convert list of tuples into normal list
    all_stations=list(np.ravel(active_stations))

    return jsonify(all_stations)


# Route with all the temperatures observed in the past year
@app.route("/api/v1.0/tobs")
def tobs():

    most_active = 'USC00519281'
    one_year_ago = '2016-08-23'
    # Create our session (link) from Python to the DB
    session=Session(engine)

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).filter(Measurement.station == most_active).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # Close our session
    session.close()
    # Create a dictionary and append to a list of all the temp obs with their date
    all_tobs = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["Temp_Obs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

# Route with Min, Avg and Max temp obs from the start date provided till the end of the date in the database
@app.route("/api/v1.0/<start>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session=Session(engine)
    
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    # Close our session
    session.close()

    # Create a dictionary and append to a list of all_stats
    all_stats = []
    for min, avg, max in start_results:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Avg"] = avg
        stats_dict["Max"] = max
        all_stats.append(stats_dict)
    return jsonify(all_stats)


# Route with Min, Avg and Max temp obs from the start date provided till the end of the date provided
@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session=Session(engine)
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter((Measurement.date <= end_date).all()
    # Close our session
    session.close()

    # Create a dictionary and append to a list of all_stats
    all_stats = []
    for min, avg, max in start_results:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Avg"] = avg
        stats_dict["Max"] = max
        all_stats.append(stats_dict)
    return jsonify(all_stats)


if __name__ == "__main__":
    app.run(debug=True)