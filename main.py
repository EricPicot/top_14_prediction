from data_preparation.data_prep import DataPrep


# ---- PARAMETERS ----
debug = False

# configuration file
dataprep_parameters_path='configurations/dataprep_parameters.yml'

# ---- DATA PREPARATION PHASE ----

# -- Create instance of DataPrep Class --
data_prep = DataPrep(dataprep_parameters_path)

data_prep.scrap(debug)

# data_prep.transform(debug)

# data_prep.load(debug)

