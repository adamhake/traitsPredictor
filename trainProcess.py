import pandas
import pickle
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, make_scorer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
class trainProcess:
	def __init__(self):
		self.data = pandas.read_csv("/Users/changye.li/Documents/scripts/traitsPredictor/clean/trainV2.csv")
		self.label = [15, 16, 17, 18, 19] ## labeled traits column indexes
		self.score = [10, 11, 12, 13, 14] ## scored traits column indexes
		self.train = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] ## train data column indexes
		## the labeled traits are [cEXT, cNEU, cAGR, cCON, cOPN] -> [15, 16, 17, 18, 19]
		## the scored traits are [sECT, sNEU, sAGR, sCON, sOPN] -> [10, 11, 12, 13, 14]
	## training model process, classification
	## store the best model
	## output: the best-fitted model for each trait
	def trainModelLabel(self):
		sample = self.data.iloc[:, self.train]
		name = ["ext", "neu", "agr", "con", "opn"]
		s = {} ## best model for each trait, with trait name as key, model as value
		## iterate each trait
		for trait in self.label:
			result = {} ## validation result
			models = {} ## store best-fitting model
			label = self.data.iloc[:, trait]
			print "processing trait: ", name[self.label.index(trait)]
			############################################################
			## SGD
			clf = linear_model.SGDClassifier(loss = "log", penalty = "elasticnet")
			scores = cross_val_score(clf, sample, label, cv = 10, scoring = "f1")
			print("SGD Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			result["SGD"] = scores.mean()
			models["SGD"] = pickle.dumps(clf)
			############################################################
			## Random Forest
			clf = RandomForestClassifier(criterion = "entropy", n_estimators = 30)
			scores = cross_val_score(clf, sample, label, cv = 10, scoring = "f1")
			print("Random Forest Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			result["RF"] = scores.mean()
			models["RF"] = pickle.dumps(clf)
			###########################################################
			## multinomial nb
			clf = MultinomialNB()
			scores = cross_val_score(clf, sample, label, cv = 10)
			print("Multinomial NB Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			result["MNB"] = scores.mean()
			models["MNB"] = pickle.dumps(clf)
			##########################################################
			## bernoulli nb
			clf = BernoulliNB()
			scores = cross_val_score(clf, sample, label, cv = 10)
			print("Bernoulli NB Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			result["BNB"] = scores.mean()
			models["BNB"] = pickle.dumps(clf)
			#########################################################
			## gradient tree boosting
			clf = GradientBoostingClassifier(loss = "deviance", n_estimators = 200, criterion = "mse")
			scores = cross_val_score(clf, sample, label, cv = 10)
			print("Gradient Boosting Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			result["GB"] = scores.mean()
			models["GB"] = pickle.dumps(clf)
			print "\n"
			## find the highest f1 score and associated model, store it to output dict
			h = max(result, key = result.get)
			s[trait] = models[h]
		return s
	## training model process, regression
	def trainModelRegression(self):
		name = ["ext", "neu", "agr", "con", "opn"]
		sample = self.data.iloc[:, self.train]
		## evaluation metrics
		mae = make_scorer(mean_absolute_error)
		mse = make_scorer(mean_squared_error)
		for trait in self.label:
			print "Processing trait: ", name[self.label.index(trait)]
			label = self.data.iloc[:, trait]
			##########################################
			## Ridge regression
			clf = linear_model.Ridge(alpha = 0.4, solver = "svd")
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("Ridge Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("Ridge Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))
			#########################################
			## Lasso regression
			clf = linear_model.Lasso(alpha = 0.8)
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("Lasso Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("Lasso Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))
			#########################################
			## Support vector regression
			clf = linear_model.SGDRegressor(loss = "huber", penalty = "elasticnet")
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("SGD Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("SGD Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))
			########################################
			## Random Forest regression
			clf = RandomForestRegressor(criterion = "mse", n_estimators = 50)
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("Random Forest Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("Random Forest Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))
			#########################################
			## KNN regression
			clf = KNeighborsRegressor(weights = "distance", algorithm = "ball_tree", p = 1, n_jobs = -1)
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("KNN Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("KNN Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))
			#########################################
			## Baysian Ridge regression
			clf = GradientBoostingRegressor(loss = "lad", n_estimators = 1000)
			score1 = cross_val_score(clf, sample, label, cv = 10, scoring = mae)
			score2 = cross_val_score(clf, sample, label, cv = 10, scoring = mse)
			print("Gradient Boosting Regression MAE: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
			print("Gradient Boosting Regression MSE: %0.2f (+/- %0.2f)" % (score2.mean(), score2.std() * 2))

			print "\n"

		
x = trainProcess()
x.trainModelRegression()