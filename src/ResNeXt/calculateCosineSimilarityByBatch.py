import scipy.io as sio
import pickle
import numpy as np
import os
import numpy as np
from sklearn.decomposition import PCA
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity

class TestCosineSimilarity(object):
	def __init__(self):
		self.name = "C2test"
		# self.name = "MSchallenge2Base"
		# self.name = "lowshotImg_cropped5_224"
		reducedDim = 512
		self.pca = PCA(n_components = reducedDim, whiten = True)

		# self.identityFeatureDir = "extracted_feature/lowshotImg_cropped5_224MeanFeature/"
		# self.PCAIdentityFeatureDir = "extracted_feature/lowshotImg_cropped5_224MeanFeaturePCA/"
		self.identityFeatureDir = "extracted_feature/MSchallenge2BaseIdentityMeanFeature/"
		self.PCAIdentityFeatureDir = "extracted_feature/MSchallenge2BaseIdentityMeanFeaturePCA/"
		# self.totalIdentityFeatureDir = "extracted_feature/Challenge2MeanFeature/"
		# self.totalIdentityFeatureDir = "extracted_feature/MSchallenge2BaseIdentityMeanFeature/"

		self.totalPCAidentityFeatureDir = "extracted_feature/Challenge2MeanFeaturePCA/"

		self.labelList = pickle.load(open(self.name + "LabelList.p", "rb"))
		print len(self.labelList)

		self.path = "extracted_feature/" + self.name + "IdentityMeanFeature/"
		if not os.path.isdir(self.path):
			os.mkdir(self.path)

	def generateIdentityFeatures(self):
		# NumtoID = pickle.load(open("MSchallenge2lowshot_224_NumtoID.p", "rb"))
		# labelList = pickle.load(open("MSchallenge2lowshot_224LabelList.p", "rb"))
		# NumtoID = pickle.load(open(name + "_NumtoID.p", "rb"))
		# print len(NumtoID)
		chunk = 5000
		maxIter = 231
		features = []
		preFeatures = []
		preLabel = None

		for iter in range(maxIter + 1):
			print "loading features....."
			print 'extracted_feature/C2test_feature/' + self.name + '_feature_batch' + str(iter) + '.txt'
			batch = np.loadtxt('extracted_feature/' + self.name + '_feature/' + self.name + '_feature_batch' + str(iter) + '.txt')
			print "finish loading features....."
			print "iter_" + str(iter), " ", batch.shape

			if iter == maxIter:
				labelList = self.labelList[iter * chunk : ]
			else:
				labelList = self.labelList[iter * chunk : (iter + 1) * chunk]

			print "len(batch): ", len(batch)
			print "len(labelList): ", len(labelList)
			if len(labelList) != len(batch):
				raise "len(labelList) != len(batch)"

			if len(preFeatures) != 0:
				features = preFeatures
			else:
				preLabel = labelList[0]
				features = []

			for index in range(len(labelList)):
				label = labelList[index]
				# print "label: ", label
				feature = batch[index]
				# print "feature.shape: ", feature.shape
				if label == preLabel:
					features.append(feature)
				else:
					features = np.asarray(features)
					identityFeature = np.mean(features, axis = 0)
					print "identityFeature.shape: ", identityFeature.shape
					sio.savemat(self.path + preLabel, {"identityFeature": identityFeature})
					print "save: ", self.path + preLabel
					preLabel = label
					features = []
					features.append(feature)
					preFeatures = []

			if len(features) != 0 and iter != maxIter:
				preFeatures = features
			else:
				features = np.asarray(features)
				identityFeature = np.mean(features, axis = 0)
				print "identityFeature.shape: ", identityFeature.shape
				sio.savemat(self.path + preLabel, {"identityFeature": identityFeature})
				print "save: ", self.path + preLabel


	def reducedIdentityDim(self):
		if not os.path.isdir(self.PCAIdentityFeatureDir):
			os.mkdir(self.PCAIdentityFeatureDir)

		identities = os.listdir(self.identityFeatureDir)
		features = []
		for identity in identities:
			print "identity: ", identity
			feature = sio.loadmat(self.identityFeatureDir + identity)["identityFeature"].flatten()
			print "feature.shape: ", feature.shape
			features.append(feature)

		print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
		features = np.asarray(features)
		print "features.shape: ", features.shape
		features = self.pca.fit_transform(features)
		print "features.shape: ", features.shape
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

		for index in range(len(identities)):
			identity = identities[index]
			feature = features[index]
			print "identity: ", identity
			print feature[:10]
			print "feature.shape: ", feature.shape
			sio.savemat(self.PCAIdentityFeatureDir + identity, {"identityFeature": feature})
			print "save: ", self.PCAIdentityFeatureDir + identity

	def reducedIdentityDimTestData(self):
		chunk = 5000
		maxIter = 23
		batches = []
		for iter in range(maxIter + 1):
			print "iter_" + str(iter)
			print "loading features....."
			print 'extracted_feature/C2test_feature/' + self.name + '_feature_batch' + str(iter) + '.txt'
			batch = np.loadtxt('extracted_feature/C2test_feature/' + self.name + '_feature_batch' + str(iter) + '.txt')
			print "batch.shape: ", batch.shape
			print "finish loading features....."
			batches.extend(batch)
			
		batches = np.asarray(batches)
		print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
		print "batches.shape: ", batches.shape
	 	batches = self.pca.fit_transform(batches)
		print "batches.shape: ", batches.shape
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

		counter = 0
		for index in range(len(batches)):
			label = labelList[index]
			feature = batch[index]
			counter += 1
			sio.savemat("extracted_feature/C2test_featurePCA/" + label, {"identityFeature": feature})
			print label
			if counter % 100 == 0:
				print counter


	def writeToFile(self, content):
		with open('mxnetPredPCA.txt', 'a') as f:
			f.write(content)

	def testCosineSimilarity(self):
		with open('mxnetPredPCA.txt', 'w') as f:
			f.write("")
		chunk = 5000
		maxIter = 23
		identities = os.listdir(self.totalPCAidentityFeatureDir)
		# identities = os.listdir(self.totalIdentityFeatureDir)
		print identities[:10]

		predcontent = ""
		counter = 0

		for iter in range(maxIter + 1):
			print "loading features....."
			print 'extracted_feature/C2test_feature/' + self.name + '_feature_batch' + str(iter) + '.txt'
			batch = np.loadtxt('extracted_feature/C2test_feature/' + self.name + '_feature_batch' + str(iter) + '.txt')
			print "finish loading features....."

			print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
			print "batch.shape: ", batch.shape
		 	batch = self.pca.fit_transform(batch)
			print "batch.shape: ", batch.shape
			print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
			print "iter_" + str(iter)

			if iter == maxIter:
				labelList = self.labelList[iter * chunk : ]
			else:
				labelList = self.labelList[iter * chunk : (iter + 1) * chunk]

			for index in range(len(labelList)):
				try:
					label = labelList[index]
					feature = batch[index]
					print "feature.shape: ", feature.shape
					# feature = self.pca.fit_transform(feature)
					# print "feature.shape: ", feature.shape
					scoreList = []
					for identity in identities:
						identityFeature = sio.loadmat(self.totalPCAidentityFeatureDir + identity)["identityFeature"]
						# identityFeature = sio.loadmat(self.totalIdentityFeatureDir + identity)["identityFeature"]
						# print identityFeature[:100]
						cosScore = 1 - float(spatial.distance.cosine(feature, identityFeature))
						# cosScore = cosine_similarity(feature, identityFeature)
						# print "identity: ", identity
						# print "cosScore: ", cosScore
						scoreList.append(cosScore)
					maxScore = max(scoreList)
					index = scoreList.index(maxScore)
					pred = identities[index]
					print "counter: ", counter
					print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
					print "label: ", label
					print "pred: ", pred
					print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
					predcontent += pred + " " + str(maxScore)
					counter += 1
					if counter % 100 == 0:
						self.writeToFile(predcontent)
						print "counter: ", counter
						content = ""
				except Exception as e:
					print e
					self.writeToFile(predcontent)
					print "counter: ", counter
					content = ""
			self.writeToFile(predcontent)
			print "counter: ", counter
			content = ""

	def run(self):
		self.reducedIdentityDimTestData()
		# self.reducedIdentityDim()
		# self.generateIdentityFeatures()
		# self.testCosineSimilarity()

if __name__ == '__main__':
	tcs = TestCosineSimilarity()
	tcs.run()
