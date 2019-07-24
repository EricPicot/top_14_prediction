# training
import pandas as pd
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
clf = tree.DecisionTreeClassifier()
clf.fit(Xtrain, ytrain)

print(clf.score(Xtest, ytest))