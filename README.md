# top_14_prediction
This repository contains a project aiming at predicting the winning team of rugby games (top 14) given a new match (ie the day and the opponents)

Given the needed features, the goal is to create a algorithm that predict the winning team of a rugby game.

## Data Preparation
The Data Preparation is performed using the `data_ETL` module.

### Raw Data scraping
Raw data is scrapped from different sources (mostly French Rugby League website: `lnr.fr`) and saved in the `/raw_data` folder.

Available datasets are :
- `matchs_results` : the results of all the TOP14 matchs since 2004/2005 
- `ranking_history` : the ranking of the team after each day
- To be continued...

### Data Transformation
Aggregations and statistical operations on raw data to extract useful features.

Operations performed :
- TBD

### Data Loading
Save the transformed data in a readable format to be used as an input for the DataScience models.

**Important note:** remember that the goal is to predict the outcome given the teams and the play day.
The loading step should return a train set and a prediction set (at least 1 line for the next match).


## Modelization



## Prediction



## User interface