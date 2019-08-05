#!/usr/bin/env python

'''A classifer to assign labels.

'''
from sklearn import preprocessing
import ast
import csv
import re
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.calibration import calibration_curve
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


feature_set = "./labeled/labeled.csv"
unlabeled_data = "./labeled/unlabeled.csv"


def load_data(crypto_file):
    return pd.read_csv(crypto_file, sep=',')

def main():

	labeled = load_data(feature_set)
	label_transform = preprocessing.LabelEncoder()
	labeled['label'] = label_transform.fit_transform(labeled['label'])
	cols = [col for col in labeled.columns if col not in ['label']]

	unlabeled = load_data(unlabeled_data)
	unlbl_cols = [unlabeled_col for unlabeled_col in unlabeled.columns]
	
	data_train, data_test, target_train, target_test = train_test_split(labeled[cols],labeled['label'], test_size = 0.30, random_state = 10)


	#create an object of the type GaussianNB
	gnb = GaussianNB()

	#create an object of type LinearSVC
	svc_model = LinearSVC(random_state=0)

	#create an object of type Random Forest
	rfc = RandomForestClassifier(n_estimators = 100)

	rfc_pred = rfc.fit(data_train, target_train).predict(data_test)
	
	#print the accuracy score of the model
	print("Random-forest accuracy : ",accuracy_score(target_test, rfc_pred, normalize = True))

	#train the algorithm on training data and predict using the testing data
	lsvc_pred = svc_model.fit(data_train, target_train).predict(data_test)
	
	#print the accuracy score of the model
	print("LinearSVC accuracy : ",accuracy_score(target_test, lsvc_pred, normalize = True))

	assigned_labels = rfc.fit(data_train, target_train).predict(unlabeled[unlbl_cols])
	print(assigned_labels)


if __name__ == '__main__':
    main()
