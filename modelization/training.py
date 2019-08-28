# training
import sys
sys.path.insert(1,'../data_preparation')
sys.path.insert(1,'../data_preparation/raw_data')

sys.path.insert(1,"../data_preparation/transformation")
import fusion_transformation as FT
from result_transformation import ResultTransformation
from ranking_transformation import RankingTransformation
import pandas as pd
import pickle 
from sklearn.model_selection import train_test_split as tts
from sklearn import tree
import os.path

print(sys.argv)

x =( sys.argv[1] )
y =( sys.argv[2] )

    
# ../data_preparation/raw_data/ranking_results.csv  ../data_preparation/raw_data/matches_results.csv
#  '../data_preparation/raw_data/matches_results.csv'
ranking_df = pd.read_csv( x, sep = "|")
Ranking = RankingTransformation()
Ranking.set_ranking_df(ranking_df)
Ranking.transform()


results_df = pd.read_csv(y, sep = "|")
Results = ResultTransformation()
Results.set_result_df(results_df)
Results.transform()

# print(Results.result_df.columns)

data = FT.merging_data(Ranking.ranking_df, Results.result_df)











columns_for_first_model = ['day_of_week_Dimanche', 
                           'day_of_week_Samedi',
                           'classement_dom',
                           "classement_ext", 
                           "win_ratio_dom",
                           "win_ratio_ext",
                           "bonus_ratio_dom",
                           "win_ratio_ext",
                           "aga_dom",
                           "aga_ext"]

X = data[columns_for_first_model]
Y = data["label"]

Xtrain,Xtest, ytrain, ytest = tts(X,Y, test_size = 0.2)
clf = tree.DecisionTreeClassifier().fit(Xtrain, ytrain)
print(clf.score(Xtest, ytest)) 


# # Save the trained model as a pickle string. 
# # from sklearn.externals import joblib 
  
# Save the model as a pickle in a file 
with open(r"models/test_model.pickle", "wb") as output_file:
    pickle.dump(clf, output_file)
print("model dumped")
# Load the pickled model 
# knn_from_pickle = pickle.loads(clf) 

# # Use the loaded pickled model to make predictions 
# knn_from_pickle.predict(X_test) 

# with open(r"someobject.pickle", "rb") as input_file:
#     loaded_model = pickle.load(input_file)
# print(loaded_model.score(Xtest, ytest)) 

data.iloc[:5,:].to_csv("test_data.csv")