# SQLAlchemy Challenge: Advanced Climate Analysis and Data Exploration


Welcome to the SQLAlchemy Challenge repository, where advanced data engineering meets climate analysis. This project leverages SQLAlchemy, a powerful SQL toolkit and Object Relational Mapper (ORM) in Python, to perform a detailed analysis of climate data, focusing on surf conditions and station observations in Hawaii.

<div align="center">
    <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot1.png" width="500" height="400">
    <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot2.png" width="500" height="400">
</div>

## Project Overview

The repository is structured to provide a comprehensive analysis through two primary components:

- **Climate Analysis Notebook (`climate_starter.ipynb`)**: A Jupyter Notebook that demonstrates the step-by-step process of querying, analyzing, and visualizing climate data. It includes detailed sections on precipitation analysis, station analysis, and temperature observation data exploration.

- **Flask API Application (`app.py`)**: A Flask web application that serves the analyzed climate data through various API endpoints. It allows users to query precipitation data, station information, and temperature observations through a user-friendly web interface.

### Featured Code Snippets

Below is a snippet of the `climate_starter.ipynb` file used in this project. 
For the complete code, please [click here](https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb).

```python
from sqlalchemy import func

most_active_station = active_stations[0][0]

# Calculate the lowest, highest, and average temperature for the most active station
lowest_temp = session.query(func.min(measurement.tobs)).\
    filter(measurement.station == most_active_station).scalar()

highest_temp = session.query(func.max(measurement.tobs)).\
    filter(measurement.station == most_active_station).scalar()

avg_temp = session.query(func.avg(measurement.tobs)).\
    filter(measurement.station == most_active_station).scalar()

print(f"Lowest Temperature: {lowest_temp}")
print(f"Highest Temperature: {highest_temp}")
print(f"Average Temperature: {avg_temp}")
```
Below is a snippet of the `app.py` file used in this project. 
For the complete code, please [click here](https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/app.py).

```python
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
```
<div align="center">
  <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot3.png" width="500" height="900">
  <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot4.png" width="500" height="900">
</div>

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Open `app.py` and modify the database connection string if necessary.
4. Run `app.py` to execute the analysis and generate the results.

## Dependencies

This project requires the following dependencies:

- Python 3.x
- SQLAlchemy
- Pandas
- Matplotlib
- Flask
