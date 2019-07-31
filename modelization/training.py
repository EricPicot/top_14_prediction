# training
import pandas as pd
import pickle 
from sklearn.model_selection import train_test_split as tts
from sklearn import tree

data = pd.read_csv("../data_preparation/raw_data/transformed_data.csv", sep = "|")

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


# Save the trained model as a pickle string. 
# from sklearn.externals import joblib 
  
# Save the model as a pickle in a file 
with open(r"models/test_model.pickle", "wb") as output_file:
    pickle.dump(clf, output_file)
print("model dumped")
# # Load the pickled model 
# knn_from_pickle = pickle.loads(saved_model) 

# # Use the loaded pickled model to make predictions 
# knn_from_pickle.predict(X_test) 

# with open(r"someobject.pickle", "rb") as input_file:
#     loaded_model = pickle.load(input_file)
# print(loaded_model.score(Xtest, ytest)) 
