import createKeyWords as CKW
import nltk.cluster.util
import numpy as np
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from time import time
import ext.common_english_words as common_english_words
import ext.extend_stop_words as custom_stop_words
from sklearn.feature_extraction import text 
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import skfuzzy as fuzz

def fuzzyCMeans(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	"""[Deprecated]
	Fuzzy C Means clustering on key-words instead of KMeans
	"""
	do_SVD = True
	words_to_show_per_cluster = 20
	number_of_clusters = 8

	keyword_dict_list, user_keyword_freq_dict, user_words_dict_list, nicks_for_stop_words = CKW.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)

	corpus = []
	for user_words_dict in user_words_dict_list:
		# print "SENDER", user_words_dict['sender']
		# print "WORDS", " ".join(user_words_dict['words'])
		corpus.append(" ".join(map(str,user_words_dict['words'])))

	print "No. of users", len(corpus)

	#TF_IDF
	stop_word_without_apostrophe=[]
	for words in common_english_words.words:
		stop_word_without_apostrophe.append(words.replace("'",""))
	
	stop_words_extended = text.ENGLISH_STOP_WORDS.union(common_english_words.words).union(nicks_for_stop_words).union(stop_word_without_apostrophe).union(custom_stop_words.words).union(custom_stop_words.slangs)
	
	vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=stop_words_extended,
																																use_idf=True)
	print "Extracting features from the training dataset using TF-IDF"
	t0 = time()
	tf_idf = vectorizer.fit_transform(corpus)
	print("done in %fs" % (time() - t0))
	print "n_samples: %d, n_features: %d \n" % tf_idf.shape

	# LSA
	if do_SVD:
		print("============USING SVD==========")
		print("Performing dimensionality reduction using LSA")
		t0 = time()
		# Vectorizer results are normalized, which makes KMeans behave as
		# spherical k-means for better results. Since LSA/SVD results are
		# not normalized, we have to redo the normalization.
		svd = TruncatedSVD(100) #recommened value = 100
		normalizer = Normalizer(copy=False)
		lsa = make_pipeline(svd, normalizer)

		tf_idf = lsa.fit_transform(tf_idf)

		print("done in %fs" % (time() - t0))

		explained_variance = svd.explained_variance_ratio_.sum()
		print("Explained variance of the SVD step: {}%".format(
						int(explained_variance * 100)))

	np.set_printoptions(threshold=np.inf)
	#clusters
	tf_idf_transpose = tf_idf.T #c-means takes the transpose
	centroids, U, U0, d, Jm, p, fpc = fuzz.cluster.cmeans(
			tf_idf_transpose, number_of_clusters, 2., error=0.005, maxiter=1000, init=None)

	print "CENTROIDS", centroids

	if do_SVD:
		original_space_centroids = svd.inverse_transform(centroids)
		order_centroids = original_space_centroids.argsort()[:, ::-1]
	else:
		order_centroids = centroids.argsort()[:, ::-1]

	print "original_space_centroids", original_space_centroids
	print "order_centroids", order_centroids

	terms = vectorizer.get_feature_names()
	for i in range(number_of_clusters):
		print("Cluster %d:" % i)
		for ind in order_centroids[i, :words_to_show_per_cluster]:
			print(' %s' % terms[ind])
		print()