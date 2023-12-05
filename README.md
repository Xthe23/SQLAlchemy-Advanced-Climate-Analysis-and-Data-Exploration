# sqlalchemy-challenge

This project focuses on using SQLAlchemy to analyze and query a database related to surf conditions.

<div align="center">
    <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot1.png" width="500" height="400">
    <img src="https://github.com/Xthe23/sqlalchemy-challenge/blob/main/SurfsUp/Resources/Screenshot2.png" width="500" height="400">
</div>

## Project Structure

The project contains the following files and directories:

- `README.md`: Provides an overview of the project and instructions on how to use it.
- `app.py`: Contains the main code for querying the database and generating analysis.
- `climate_analysis.ipynb`: A Jupyter Notebook file that demonstrates the analysis process step-by-step.
- `Resources/`: A directory that contains the sqlite database file and CSV data files used in the analysis.

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
