import createKeyWords as CKW
import nltk.cluster.util
import numpy
import math

def svdOnKeywords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	'''
		each user's normalised frequency stored in rows
		all the keywords (unfiltered)
	'''
	keyword_list = []
	user_list = []

	keyword_dict_list, user_keyword_freq_dict = CKW.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)

	for dictionary in user_keyword_freq_dict:
		# print dictionary['keywords']
		keyword_list = list(set(keyword_list + [x[0] for x in  dictionary['keywords']]))

	# print user_keyword_freq_dict #(Format : [<word>, <frequency>, <normalised_score>])'
	user_keyword_normalfreq_matrix = []
	user_keyword_freq_matrix_for_doc_ = []
	keyword_for_user = []

	for user_tuple in user_keyword_freq_dict:
		nick =  user_tuple['nick']
		keywords =  user_tuple['keywords']
		user_list.append(nick)

		N = 0
		temp = 0
		'''calculete N = (summation of ni**2)**1/2'''
		for keyword in keywords:
			temp += keyword[1]**2

		N = math.sqrt(temp)
		temp = []
		keyword_normal_freq_for_user = [0 for i in xrange(len(keyword_list))] #to be used as column
		
		for keyword_tuple in keywords:
			keyword = keyword_tuple[0]
			normal_freq = keyword_tuple[1]/N
			keyword_normal_freq_for_user[keyword_list.index(keyword)] = normal_freq
			for i in xrange(0,keyword_tuple[1]):
				temp.append(keyword)
		
		keyword_for_user.append(temp)
		user_keyword_normalfreq_matrix.append(keyword_normal_freq_for_user)

	# print len(user_list)
	# print len(keyword_list)
	# print keyword_for_user
	# print user_keyword_normalfreq_matrix
	# print len(user_keyword_normalfreq_matrix )

	'''
		IF-IDF
		https://stanford.edu/~rjweiss/public_html/IRiSS2013/text2/notebooks/tfidf.html
	'''
	mydoclist = keyword_for_user
	vocabulary = keyword_list
	doc_term_matrix = []

	def l2_normalizer(vec):
		denom = numpy.sum([el**2 for el in vec])
		return [(el / math.sqrt(denom)) for el in vec]

	def tf(term, document):
		return freq(term, document)

	def freq(term, document):
		return document.count(term)

	for doc in mydoclist:
		print 'The doc is "' + ",".join(doc)+ '"'
		tf_vector = [tf(word, doc) for word in vocabulary]
		tf_vector_string = ', '.join(format(freq, 'd') for freq in tf_vector)
		print 'The tf vector for Document %d is [%s]' % ((mydoclist.index(doc)+1), tf_vector_string)
		doc_term_matrix.append(tf_vector)

	def numDocsContaining(word, doclist):
		doccount = 0
		for doc in doclist:
			if freq(word, doc) > 0:
				doccount +=1
		return doccount 

	def idf(word, doclist):
		n_samples = len(doclist)
		df = numDocsContaining(word, doclist)
		return numpy.log(n_samples / 1+df)

	my_idf_vector = [idf(word, mydoclist) for word in vocabulary]

	# print 'Our vocabulary vector is [' + ', '.join(list(vocabulary)) + ']'
	# print 'The inverse document frequency vector is [' + ', '.join(format(freq, 'f') for freq in my_idf_vector) + ']'

	def build_idf_matrix(idf_vector):
		idf_mat = numpy.zeros((len(idf_vector), len(idf_vector)))
		numpy.fill_diagonal(idf_mat, idf_vector)
		return idf_mat

	my_idf_matrix = build_idf_matrix(my_idf_vector)

	print "idf-matrix" , my_idf_matrix

	 # Now we have converted our IDF vector into a matrix of size BxB, where the diagonal is the IDF vector. That means we can perform now multiply every term frequency vector by the inverse document frequency matrix. Then to make sure we are also accounting for words that appear too frequently within documents, we'll normalize each document such that the L2 norm = 1.
	doc_term_matrix_tfidf = []

	#performing tf-idf matrix multiplication
	for tf_vector in doc_term_matrix:
		doc_term_matrix_tfidf.append(numpy.dot(tf_vector, my_idf_matrix))

	#normalizing
	doc_term_matrix_tfidf_l2 = []
	for tf_vector in doc_term_matrix_tfidf:
		doc_term_matrix_tfidf_l2.append(l2_normalizer(tf_vector))
																			
	print vocabulary
	print doc_term_matrix_tfidf_l2# np.matrix() just to make it easier to look at

	'''
		SVD
	'''
	# clusterer = nltk.cluster.util.VectorSpaceClusterer(normalise=False, svd_dimensions=25)#http://www.nltk.org/_modules/nltk/cluster/util.html
	# clusterer.cluster(user_keyword_normalfreq_matrix)

	#borrow cluster code from http://www.nltk.org/_modules/nltk/cluster/util.html

	svd_dimensions = 5
	# vectors = user_keyword_normalfreq_matrix
	# vectors = doc_term_matrix_tfidf_l2
	vectors = doc_term_matrix_tfidf

	if svd_dimensions and svd_dimensions < len(vectors[0]):
		[u, d, vt] = numpy.linalg.svd(numpy.transpose(numpy.array(vectors)))
		S = d[:svd_dimensions] * \
		numpy.identity(svd_dimensions, numpy.float64)
		T = u[:,:svd_dimensions]
		Dt = vt[:svd_dimensions,:]
		vectors = numpy.transpose(numpy.dot(S, Dt))

		print "S", S
		print "T", T
		print "Dt", Dt