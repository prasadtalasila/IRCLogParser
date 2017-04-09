import networkx as nx
import re
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text 
import ext.common_english_words as common_english_words
import ext.extend_stop_words as custom_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from time import time
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import util

sys.path.append('../lib')
import config
import util
sys.path.append('../..')
import ext
import ext.common_english_words as common_english_words
import ext.extend_stop_words as custom_stop_words


def nick_change_graph(log_dict, DAY_BY_DAY_ANALYSIS=False):

    """ creates a graph which tracks the nick changes of the users
    where each edge has a time stamp denoting the time 
    at which the nick was changed by the user

    Args:
        log_dict (str): Dictionary of logs created using reader.py    

    Returns:
       list of the day_to_day nick changes if config.DAY_BY_DAY_ANALYSIS=True or else an aggregate nick change graph for the 
       given time period.
    """     

    rem_time = None #remembers the time of the last message of the file parsed before the current file
    nick_change_day_list = []
    aggregate_nick_change_graph = nx.MultiDiGraph() # graph for nick changes in the whole time span (not day to day)
    
    for day_content_all_channels in log_dict.values():      
        
        for day_content in day_content_all_channels:            
                day_log = day_content["log_data"]                   
                
                today_nick_change_graph = nx.MultiDiGraph()   #using networkx
                current_line_no = -1
                
                for line in day_log:
                    current_line_no = current_line_no + 1
                    
                    if(line[0] == '=' and "changed the topic of" not in line):  #excluding the condition when user changes the topic. Search for only nick changes
                        nick1 = util.splice_find(line, "=", " is", 3)
                        nick2 = util.splice_find(line, "wn as", "\n", 5)                        
                        earlier_line_no = current_line_no

                        while earlier_line_no >= 0: #to find the line just before "=="" so as to find time of Nick Change
                            earlier_line_no = earlier_line_no - 1
                            if(day_log[earlier_line_no][0] != '='):                             
                                year, month, day = util.get_year_month_day(day_content)
                                util.build_graphs(nick1, nick2, day_log[earlier_line_no][1:6], year, month, day, today_nick_change_graph, aggregate_nick_change_graph)
                                break

                        if(earlier_line_no == -1):
                            today_nick_change_graph.add_edge(nick1, nick2, weight=rem_time)                                              
                            aggregate_nick_change_graph.add_edge(nick1, nick2, weight = rem_time)
                
                count = len(day_log) - 1 #setting up the rem_time for next file, by noting the last message sent on that file.
                
                while(count >= 0):
                    if(day_log[count][0] != '='):
                        rem_time = day_log[count][1:6]
                        break
                    count = count-1
                
                nick_change_day_list.append(today_nick_change_graph)    
                        
    if DAY_BY_DAY_ANALYSIS:
        return nick_change_day_list
    else:
        return aggregate_nick_change_graph
            

def top_keywords_for_nick(user_keyword_freq_dict, nick, threshold, min_words_spoken): 
    """ 
    outputs top keywords for a particular nick

    Args:
        user_keyword_freq_dict(dict): dictionary for each user having keywords and their frequency
        nick(str) : user to do analysis on
        threshold(float): threshold on normalised values to seperate meaningful words
        min_words_spoken(int): threhold on the minumum number of words spoken by a user to perform analysis on

    Returns:
       null 

    """

    keywords = None
    for dicts in user_keyword_freq_dict:
        if dicts['nick'] == nick:
            keywords = dicts['keywords']
            break
    
    total_freq = 0.0
    for freq_tuple in keywords:
        total_freq += freq_tuple[1]

    top_keywords = []
    top_keywords_normal_freq = []
    
    if total_freq > min_words_spoken:
        if keywords:
            for keyword in keywords:
                if keyword[2] >= threshold:
                        top_keywords.append(keyword[0].encode('ascii', 'ignore'))
                        top_keywords_normal_freq.append(keyword[2])

            if len(top_keywords) == 0:
                if config.DEBUGGER and config.PRINT_WORDS:
                    print "No word's normalised score crosses the value of", threshold
                top_keywords = None
        else:
            if config.DEBUGGER and config.PRINT_WORDS:
                print "No message sent by nick", nick
            pass
    else:
        if config.DEBUGGER and config.PRINT_WORDS:
            print "Not enough words spoken by", nick, "; spoke" ,int(total_freq), "words only, required", min_words_spoken
        pass

    return (top_keywords, top_keywords_normal_freq)


def keywords(log_dict, nicks, nick_same_list):
    """
    Returns keywods for all users

    Args:   
        log_dict (str): Dictionary of logs data created using reader.py
        nicks(List) : list of nickname created using nickTracker.py
        nick_same_list :List of same_nick names created using nickTracker.py

    Returns
        keywords_filtered: filtered keywords for user
        user_keyword_freq_dict: dictionary for each user having keywords and their frequency
        user_words_dict: keywods for user
        nicks_for_stop_words: stop words
    """
    user_words_dict = []
    user_keyword_freq_dict = []
    keywords_filtered = []
    no_messages = 0    

    def get_nick_receiver(nick_receiver, rec, nick_to_compare, nick_name, nicks, nick_same_list):              
        if(rec == nick_name):
            if(nick_to_compare != nick_name):                
                nick_receiver = util.get_nick_representative(nicks, nick_same_list, nick_name)        
        return nick_receiver           

    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            for line in day_log:
                flag_comma = 0
                if(util.check_if_msg_line(line)):
                    m = re.search(r"\<(.*?)\>", line)
                    nick_to_compare = util.correctLastCharCR((m.group(0)[1:-1]))
                    nick_sender = ''                    
                    nick_sender = util.get_nick_representative(nicks, nick_same_list, nick_to_compare)
                    
                    nick_receiver = ''
                    for nick_name in nicks:
                        rec_list = [e.strip() for e in line.split(':')] #receiver list splited about :
                        util.rec_list_splice(rec_list)
                        if not rec_list[1]: #index 0 will contain time 14:02
                            break                        
                        rec_list = util.correct_last_char_list(rec_list)        
                        for rec in rec_list:
                            nick_receiver = get_nick_receiver(nick_receiver, rec, nick_to_compare, nick_name, nicks, nick_same_list)                            
                
                        if "," in rec_list[1]:  #receiver list may of the form <Dhruv> Rohan, Ram :
                            flag_comma = 1
                            rec_list_2 = [e.strip() for e in rec_list[1].split(',')]                            
                            rec_list_2 = util.correct_last_char_list(rec_list_2)        
                            for rec in rec_list_2:
                                nick_receiver = get_nick_receiver(nick_receiver, rec, nick_to_compare, nick_name, nicks, nick_same_list)                                

                        if(flag_comma == 0): #receiver list can be <Dhruv> Rohan, Hi!
                            rec = util.splice_find(line, ">", ", ", 1)                            
                            nick_receiver = get_nick_receiver(nick_receiver, rec, nick_to_compare, nick_name, nicks, nick_same_list)                           
                                            
                    
                    #generating the words written by the sender
                    message = rec_list[1:]
                    no_messages += 1
                    correctedNickReciever = util.correct_nick_for_(nick_receiver)
                    if correctedNickReciever in message:
                        message.remove(correctedNickReciever)

                    lmtzr = WordNetLemmatizer()
                    
                    #limit word size = 3, drop numbers.
                    word_list_temp = re.sub(r'\d+', '', " ".join(re.findall(r'\w{3,}', ":".join(message).replace(","," ")))).split(" ")
                    word_list = []
                    
                    #remove punctuations
                    for word in word_list_temp:
                        word = word.lower()
                        word_list.append(word.replace("'",""))
                    word_list_lemmatized = []
                    
                    try:     
                        word_list_lemmatized = map(lmtzr.lemmatize, map(lambda x: lmtzr.lemmatize(x, 'v'), word_list))
                    except UnicodeDecodeError:
                        pass

                    fr = 1
                    for dic in user_words_dict:
                        if dic['sender'] == nick_sender:
                                dic['words'].extend(word_list_lemmatized)
                                fr = 0
                    if fr:
                        user_words_dict.append({'sender':nick_sender, 'words':word_list_lemmatized }) 

    nicks_for_stop_words = []
    stop_word_without_apostrophe = []

    for l in nick_same_list:
        nicks_for_stop_words.extend(l)

    for dictonary in user_words_dict:
        nicks_for_stop_words.append(dictonary['sender'])

    nicks_for_stop_words.extend([x.lower() for x in nicks_for_stop_words])

    for words in common_english_words.words:
        stop_word_without_apostrophe.append(words.replace("'",""))        
    
    stop_words_extended = extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe)

    count_vect = CountVectorizer(analyzer = 'word', stop_words=stop_words_extended, min_df = 1)
    keywords_for_channels = []
    for dictonary in user_words_dict:
        try:
            matrix = count_vect.fit_transform(dictonary['words'])
            freqs = [[word, matrix.getcol(idx).sum()] for word, idx in count_vect.vocabulary_.items()]
            keywords = sorted(freqs, key = lambda x: -x[1])
            total_freq = 0.0
            for freq_tuple in keywords:
                total_freq += freq_tuple[1]
            
            for freq_tuple in keywords:
                freq_tuple.append(round(freq_tuple[1]/float(total_freq), 5))
            user_keyword_freq_dict.append({'nick':dictonary['sender'], 'keywords': keywords })
            keywords_for_channels.extend(keywords)
        except ValueError:
                pass
    for data in user_keyword_freq_dict:
        keywords, normal_scores = top_keywords_for_nick(user_keyword_freq_dict, data['nick'], config.KEYWORDS_THRESHOLD, config.KEYWORDS_MIN_WORDS)
        if config.DEBUGGER and config.PRINT_WORDS:    
            print "Nick:", data['nick']
            print "Keywords with normalised score > 0.01\n", keywords
            print "Their Normal scores\n", normal_scores
            print "\n"
        if keywords:
            keywords_filtered.append({'nick': data['nick'], 'keywords': keywords})
    
    return keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted(keywords_for_channels, key = lambda x: x[2], reverse=True)


def keywords_clusters(log_dict, nicks, nick_same_list):
    """ 
        Uses `keywords` to form clusters of words post TF IDF (optional).

    Args:   
        log_dict (str): Dictionary of logs data created using reader.py
        nicks(List) : list of nickname created using nickTracker.py
        nick_same_list :List of same_nick names created using nickTracker.py

    Returns
        null
    """

    '''
        AUTO TFIDF FROM JUST SENTENCES
    '''
    #http://scikit-learn.org/stable/auto_examples/text/document_clustering.html
    #BUILDING CORPUS

    keyword_dict_list, user_keyword_freq_dict, user_words_dict_list, nicks_for_stop_words, keywords_for_channels = keywords(log_dict, nicks, nick_same_list)

    corpus = []

    def build_centroid(km):
        if config.ENABLE_SVD:
            original_space_centroids = svd.inverse_transform(km.cluster_centers_)
            order_centroids = original_space_centroids.argsort()[:, ::-1]
        else:
            order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        return order_centroids

    for user_words_dict in user_words_dict_list:
        corpus.append(" ".join(map(str,user_words_dict['words'])))

    print "No. of users", len(corpus)

    #TF_IDF
    stop_word_without_apostrophe = []
    for words in common_english_words.words:
        stop_word_without_apostrophe.append(words.replace("'",""))

    stop_words_extended = extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe) 
    
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=stop_words_extended,
                                                                 use_idf=True)
    print "Extracting features from the training dataset using TF-IDF"
    t0 = time()
    tf_idf = vectorizer.fit_transform(corpus)
    print("done in %fs" % (time() - t0))
    print "n_samples: %d, n_features: %d \n" % tf_idf.shape

    # LSA
    if config.ENABLE_SVD:
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

    if not config.ENABLE_ELBOW_METHOD_FOR_K:
        # CLUSTERING
        km = KMeans(n_clusters=config.NUMBER_OF_CLUSTERS, init='k-means++',
                    random_state=3465, max_iter=100, n_init=8)

        print("Clustering sparse data with %s" % km)
        t0 = time()
        km.fit(tf_idf)
        print("done in %0.3fs" % (time() - t0))
        print("Top terms per cluster:")        
        
        order_centroids = build_centroid(km)            
        np.set_printoptions(threshold=np.nan)

        terms = vectorizer.get_feature_names()
        for i in range(config.NUMBER_OF_CLUSTERS):
                print("Cluster %d:" % i)
                for ind in order_centroids[i, :config.SHOW_N_WORDS_PER_CLUSTER]:
                        print terms[ind]+"\t"+str(round(km.cluster_centers_[i][ind], 2))
                print ""

    else:
        print "============ELBOW METHOD ============="

        sum_squared_errors_list = []
        avg_sum_squared_errors_list = []

        for i in xrange(1, config.CHECK_K_TILL + 1):

            print "\n===>> K = ", i

            km = KMeans(n_clusters=i, init='k-means++', max_iter=100, n_init=8)

            t0 = time()
            km.fit(tf_idf)
           
            order_centroids = build_centroid(km)

            distance_matrix_all_combination = cdist(tf_idf, km.cluster_centers_, 'euclidean')
            # cIdx = np.argmin(distance_matrix_all_combination,axis=1)
            distance_from_nearest_centroid = np.min(distance_matrix_all_combination, axis=1)
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
                    for ind in order_centroids[i, :config.SHOW_N_WORDS_PER_CLUSTER]:
                            print(' %s' % terms[ind])
                    print()

        plt.plot(range(1, config.CHECK_K_TILL+1), sum_squared_errors_list, 'b*-')
        # ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
        # markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
        plt.grid(True)
        plt.xlabel('Number of clusters')
        plt.ylabel('Average sum of squares')
        plt.title('Elbow for KMeans clustering')
        plt.show()

        #NOTE RANDOM OUTPUTS BECAUSE OF RANDOM INITIALISATION
        print "NOTE RANDOM OUTPUTS BECAUSE OF RANDOM INITIALISATION"

def extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe):
    stop_words_extended = text.ENGLISH_STOP_WORDS.union(common_english_words.words).union(nicks_for_stop_words).union(stop_word_without_apostrophe).union(custom_stop_words.words).union(custom_stop_words.slangs)
    return stop_words_extended