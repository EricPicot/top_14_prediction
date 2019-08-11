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

### Primary Data Transformation and fusion
Aggregations and statistical operations on raw data to extract useful features.

First, a transformation is done seperately on the results data and on the ranking data. 
The two classes `ResultsTransformation` and `RankingTransformation` are built to do so.

Then, those two datasets are merge on the following columns in `FusionTransformation`:
- `season_id`
- `season_day`
- `team`

**Notes :**
- The season_day of the ranking data must match with the following season_day of the result data, because ranking information of a given day must be an input for the following day games. Therefore a column `season_day+1` is temporary created in the ranking data
- Secondary transformations needs to be done. Example: the frequency of Bonus point of a team, the win ratio, etc.... It will be done via another set of method (@Gui, c'est ce dont on parlait, histoire de donner en entrée des valeurs simples, et que les features soient calculées après


### Data Loading
`FusionTransformation` must be call to compute all necessary primary transformations.

After the data has been loaded, secondary transformation must be done to create new meaningful features. `FeatureCreation` must be called
**Important note:** remember that the goal is to predict the outcome given the teams and the play day.
The loading step should return a train set and a prediction set (at least 1 line for the next match).


## Modelization




## Prediction



## User interface
