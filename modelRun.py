import os
import csv
import pandas as pd 
import pickle
from sklearn import preprocessing
from trainProcess import trainProcess
from trainBuild import trainBuild
class modelRun:
	def __init__(self):
		self.path = "/Users/changye.li/Documents/scripts/traitsPredictor/clean/"
	## get the list of all docs 
	# output: list that contains testing filenames
	def getDocs(self):
		docs = []
		for r, d ,f in os.walk(self.path):
			for files in f:
				if files.endswith(".csv"):
					docs.append(files)
		return docs
	## get attribute vector for each test user
	# output: normalized dataframe, which each entry represents user's attribute
	def processFiles(self):
		docs = self.getDocs()
		attr = []
		for each in docs:
			print "processing file: ", each
			df = pd.read_csv(self.path + each)
			attr.append(df.sum(axis = 0).values.tolist())
		attr = pd.DataFrame(attr)
		## normalization
		attr = preprocessing.normalize(attr)
		return attr
	## get prediction from trained model
	# output: list of five list, which each sublist is the predicted label for each trait
	def getLabel(self):
		attr = self.processFiles()
		traits = ["EXT", "NEU", "AGR", "CON", "OPN"]
		pre = {} ## store predictions for each trait
		## get trained model
		x = trainProcess()
		files = x.readFiles()
		tokens = x.processData()
		dff = x.getAttr(tokens)
		models = x.trainModel(dff, files)
		print attr
		for item in traits:
			clf = pickle.loads(models[item])
			pre[item] = clf.predict(attr)
		for k, v in pre.iteritems():
			print k, v
	## get scores from training data
	# output: user scores for each trait
	def getScore(self):
		y = trainBuild()
		y.readFiles()
		df1 = y.process()
		score = y.group(df1)



## test
x = modelRun()
x.getLabel()