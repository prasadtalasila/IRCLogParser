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

def keyWordsCluster_KMeansTFIDF(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	""" Uses `createKeyWords` to form clusters of words post TF IDF (optional).

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        channel_name (str): Channel to be perform analysis on
        output_directory (str): Location of output directory
        startingDate (int): Date to start the analysis (in conjunction with startingMonth)
        startingMonth (int): Date to start the analysis (in conjunction with startingDate)
        endingDate (int): Date to end the analysis (in conjunction with endingMonth)
        endingMonth (int): Date to end the analysis (in conjunction with endingDate)

    Returns:
       null 

    """
	do_SVD = False
	words_to_show_per_cluster = 10
	elbow_method_for_finding_K = False
	
	'''NON ELBOW'''
	number_of_clusters = 11 #elbow for jan-2013 = 
	
	'''ELBOW SETTINGS'''
	check_k_till = 20
	
	'''
		MANUALLY CREATING A MATRIX
	'''

	#   each user's normalised frequency stored in rows
	#   all the keywords (unfiltered)
	# '''
	# keyword_list = []
	# user_list = []

	# keyword_dict_list, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words = CKW.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)

	# for dictionary in user_keyword_freq_dict:
	#   # print dictionary['keywords']
	#   keyword_list = list(set(keyword_list + [x[0] for x in  dictionary['keywords']]))
	#   user_list.append(dictionary['nick'])

	# # print "\n \n \n", "KEYWORDS_LIST", keyword_list
	# # print "\n \n \n", "USER_LIST", user_list


	# #GENERATE A MATRIX WITH USERS AS ROWS AND KEYWORDS AS COLUMNS
	# user_keyword_matrix = np.zeros(shape=(len(user_list), len(keyword_list)))
	# # user_keyword_matrix = [[0]*len(keyword_list) for _ in xrange(len(user_list))]


	# for dictionary in user_keyword_freq_dict:
	#   # print dictionary['nick'], user_list.index(dictionary['nick'])
	#   for word_tuple in dictionary['keywords']:
	#     # print word_tuple, keyword_list.index(word_tuple[0])
	#     user_keyword_matrix[user_list.index(dictionary['nick'])][keyword_list.index(word_tuple[0])] += word_tuple[1]

	# print user_keyword_matrix

	# transformer = TfidfTransformer()
	# tfidf = transformer.fit_transform(user_keyword_matrix)
	# tfIDFMatrix = tfidf.toarray()

	# print np.nonzero(tfIDFMatrix)

	# # Each row is normalized to have unit euclidean norm. 
	# # The weights of each feature computed by the fit method call are stored in a model attribute:
	# print "Weights of each feature", transformer.idf_   
	# for i in xrange(len(transformer.idf_)):
	#   print keyword_list[i], transformer.idf_[i]        
	#   
	#  
	 
	
	'''
		AUTO TFIDF FROM JUST SENTENCES
	'''
	#http://scikit-learn.org/stable/auto_examples/text/document_clustering.html
	#BUILDING CORPUS

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


	if not elbow_method_for_finding_K:
		# CLUSTERING
		km = KMeans(n_clusters=number_of_clusters, init='k-means++',random_state=3465 ,max_iter=100, n_init=8)

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(tf_idf)
		print("done in %0.3fs" % (time() - t0))


		print("Top terms per cluster:")
		if do_SVD:
			original_space_centroids = svd.inverse_transform(km.cluster_centers_)
			order_centroids = original_space_centroids.argsort()[:, ::-1]
		else:
			order_centroids = km.cluster_centers_.argsort()[:, ::-1]
		np.set_printoptions(threshold=np.nan)

		terms = vectorizer.get_feature_names()
		for i in range(number_of_clusters):
				print("Cluster %d:" % i)
				for ind in order_centroids[i, :words_to_show_per_cluster]:
						print terms[ind]+"\t"+str(round(km.cluster_centers_[i][ind],2))
				print ""

	else:
		print "============ELBOW METHOD ============="

		sum_squared_errors_list = []
		avg_sum_squared_errors_list = []

		for i in xrange(1,check_k_till+1):

			print "\n===>> K = ", i

			km = KMeans(n_clusters=i, init='k-means++', max_iter=100, n_init=8)

			t0 = time()
			km.fit(tf_idf)

			if do_SVD:
				original_space_centroids = svd.inverse_transform(km.cluster_centers_)
				order_centroids = original_space_centroids.argsort()[:, ::-1]
			else:
				order_centroids = km.cluster_centers_.argsort()[:, ::-1]

			distance_matrix_all_combination = cdist(tf_idf, km.cluster_centers_, 'euclidean')
			# cIdx = np.argmin(distance_matrix_all_combination,axis=1)
			distance_from_nearest_centroid = np.min(distance_matrix_all_combination,axis=1)
			sum_squared_errors = sum(distance_from_nearest_centroid)
			avg_sum_squared_errors = sum_squared_errors/tf_idf.shape[0] 

			print "Sum Squared Error =", sum_squared_errors
			print "Avg Sum Squared Error =", avg_sum_squared_errors

			sum_squared_errors_list.append(sum_squared_errors)
			avg_sum_squared_errors_list.append(avg_sum_squared_errors)
			print("Top terms per cluster:")
			terms = vectorizer.get_feature_names()
			for i in range(i):
					print("Cluster %d:" % i)
					for ind in order_centroids[i, :words_to_show_per_cluster]:
							print(' %s' % terms[ind])
					print()

		plt.plot(range(1,check_k_till+1), sum_squared_errors_list, 'b*-')
		# ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
		# markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
		plt.grid(True)
		plt.xlabel('Number of clusters')
		plt.ylabel('Average sum of squares')
		plt.title('Elbow for KMeans clustering')
		
		plt.savefig(output_directory+'key-words/'+'elbow_KMeans.png')
		plt.show()

		#NOTE RANDOM OUTPUTS BECAUSE OF RANDOM INITIALISATION
		print "NOTE RANDOM OUTPUTS BECAUSE OF RANDOM INITIALISATION"