import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from sklearn.utils import shuffle

def build_model():
    df = pd.read_csv('Fundraising.csv')
    X = df.drop(['TARGET_B','Row Id','Row Id.','TARGET_D'],axis=1)
    y= df['TARGET_B']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,random_state=12345)

    clf1 = RandomForestClassifier(n_estimators=210,max_depth=3)
    clf2 = MLPClassifier(activation='logistic',solver='lbfgs',hidden_layer_sizes=(1000, 1500), random_state=101)
    clf3 = KNeighborsClassifier(n_neighbors=50)
    clf = VotingClassifier(estimators=[('lr1', clf1), ('mlp', clf2), ('knn',clf3)], voting='hard')
    clf.fit(X_train,y_train)
    predicted = clf.predict(X_test)

    df1  = df[df['TARGET_B'] == 1].sample(frac=0.051,random_state=12345)
    df2 = df[df['TARGET_B'] == 0].sample(frac=0.949,random_state=12345)
    frames = [df1, df2]

    df = pd.concat(frames)
    df = shuffle(df)

    X = df.drop(['TARGET_B','Row Id','Row Id.','TARGET_D'],axis=1)
    y= df['TARGET_B']
    return clf


def import_model():
    pickle_file = open('VotingClassifierModel.sav','rb')
    clf = pickle.load(pickle_file)
    pickle_file.close()
    return clf
