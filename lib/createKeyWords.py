import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text 
import ext.common_english_words as common_english_words
import ext.extend_stop_words as custom_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import string
import re
import ext.util

def correctNickFor_(inText):#last letter of nick maybe _ and this produces error in nickmatching
	if(inText and inText[len(inText)-1]=='_'):
		inText = inText[:-1]
	return inText

def dataForNick(data, nick, threshold, min_words_spoken): 
	keywords = None
	for dicts in data:
		if dicts['nick'] == nick:
			keywords = dicts['keywords']
			break
	total_freq = 0.0
	for freq_tuple in keywords:
		total_freq+=freq_tuple[1]
	selected_keywords = []
	selected_keywords_normal_freq = []
	if total_freq > min_words_spoken:
		if keywords:
			# selected_keywords = [keyword for keyword in keywords if keyword[2] >= threshold]
			# selected_keywords = [keyword[0].encode('ascii', 'ignore') for keyword in keywords if keyword[2] >= threshold]
			for keyword in keywords:
				if keyword[2] >= threshold:
						selected_keywords.append(keyword[0].encode('ascii', 'ignore'))
						selected_keywords_normal_freq.append(keyword[2])

			if len(selected_keywords) == 0:
				# print "No word's normalised score crosses the value of", threshold
				selected_keywords = None
		else:
			# print "No message sent by nick", nick
			pass
	else:
		# print "Not enough words spoken by", nick, "; spoke" ,int(total_freq), "words only, required", min_words_spoken
		pass
	return (selected_keywords, selected_keywords_normal_freq)

def createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	""" outputs the keywords for each user on a particular channel
	after normalising the frequency and removing the common stop words.

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

	out_dir_nick_change = output_directory+"key-words/"
	user_words_dict = []
	user_keyword_freq_dict = []
	nick_same_list=[[] for i in range(5000)] #list of list with each list having all the nicks for that particular person
	keywords_filtered = []
	no_messages = 0

	# print "Creating a new output folder"
	# os.system("rm -rf "+out_dir_nick_change)
	# os.system("mkdir "+out_dir_nick_change)

	rem_time= None #remembers the time of the last message of the file parsed before the current file

	for folderiterator in range(startingMonth, endingMonth + 1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name
			
			# print "Analysing ",filePath 
			
			nicks = [] #list of all the nicknames     
			'''
				Getting all the nicknames in a list nicks[]
			'''
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks:                       
						nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks)):
				nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
					
			for i in xrange(0,len(nicks)):
				nicks[i]=ext.util.correctLastCharCR(nicks[i])

			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line): #excluding the condition when user changes the topic. Search for only nick changes
					nick1=ext.util.correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
					nick2=ext.util.correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
					if nick1 not in nicks:
						nicks.append(nick1)
					if nick2 not in nicks:
						nicks.append(nick2)
				
			#print("printing nicks***********************************")
			#print(nicks)	
			'''
				Forming list of lists for avoiding nickname duplicacy
			'''
			
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					line1=line[line.find("=")+1:line.find(" is")][3:]
					line2=line[line.find("wn as")+1:line.find("\n")][5:]
					line1=ext.util.correctLastCharCR(line1)
					line2=ext.util.correctLastCharCR(line2)
					for i in range(5000):
						if line1 in nick_same_list[i] or line2 in nick_same_list[i]:
							nick_same_list[i].append(line1)
							nick_same_list[i].append(line2)
							break
						if not nick_same_list[i]:
							nick_same_list[i].append(line1)
							nick_same_list[i].append(line2)
							break
			#print("printing nick_same_list****************************")
			#print(nick_same_list)     
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var = ext.util.correctLastCharCR(var)
					for d in range(len(nicks)):
						if var in nick_same_list[d]:
							nick_sender = nick_same_list[d][0]
							break
						else:
							nick_sender = var
					
					nick_receiver=''
					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')] #receiver list splited about :
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]: #index 0 will contain time 14:02
							break
						for k in xrange(0,len(rec_list)):
							if(rec_list[k]): #checking for \
								rec_list[k] = ext.util.correctLastCharCR(rec_list[k])
						for z in rec_list:
							if(z==i):
								if(var != i):  
									for d in range(len(nicks)):
										if i in nick_same_list[d]:
											nick_receiver=nick_same_list[d][0]
											break
										else:
											nick_receiver=i
				
						if "," in rec_list[1]: #receiver list may of the form <Dhruv> Rohan, Ram :
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for y in xrange(0,len(rec_list_2)):
								if(rec_list_2[y]): #checking for \
									rec_list_2[y]=ext.util.correctLastCharCR(rec_list_2[y])
							for j in rec_list_2:
								if(j==i):
									if(var != i):   
										for d in range(len(nicks)):
											if i in nick_same_list[d]:
												nick_receiver=nick_same_list[d][0]
												break
											else:
												nick_receiver=i  

						if(flag_comma == 0): #receiver list can be <Dhruv> Rohan, Hi!
							rec=line[line.find(">")+1:line.find(", ")] 
							rec=rec[1:]
							rec=ext.util.correctLastCharCR(rec)
							if(rec==i):
								if(var != i):
									for d in range(len(nicks)):
										if i in nick_same_list[d]:
											nick_receiver=nick_same_list[d][0]
											break
										else:
											nick_receiver=i
					
					#generating the words written by the sender
					message = rec_list[1:]
					no_messages += 1
					correctedNickReciever = correctNickFor_(nick_receiver)
					if correctedNickReciever in message:
						message.remove(correctedNickReciever)
					# print nick_sender, "Message", ":".join(message), "end"  

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
					# word_list_lemmatized = [ unicode(s) for s in word_list_lemmatized]
					# print "=====>original", word_list
					# print "===>lemmatized", word_list_lemmatized

					fr = 1
					for dic in user_words_dict:
						if dic['sender'] == nick_sender:
								# print '1========',word_list_lemmatized
								dic['words'].extend(word_list_lemmatized)
								fr = 0
					if fr:
						# print '2========',word_list_lemmatized
						user_words_dict.append({'sender':nick_sender, 'words':word_list_lemmatized }) 

	nicks_for_stop_words = []
	stop_word_without_apostrophe=[]

	for l in nick_same_list:
		nicks_for_stop_words.extend(l)

	for dictonary in user_words_dict:
		nicks_for_stop_words.append(dictonary['sender'])

	nicks_for_stop_words.extend([x.lower() for x in nicks_for_stop_words])

	for words in common_english_words.words:
		stop_word_without_apostrophe.append(words.replace("'",""))
		
	stop_words_extended = text.ENGLISH_STOP_WORDS.union(common_english_words.words).union(nicks_for_stop_words).union(stop_word_without_apostrophe).union(custom_stop_words.words).union(custom_stop_words.slangs)
	count_vect = CountVectorizer(analyzer = 'word', stop_words=stop_words_extended, min_df = 1)

	for dictonary in user_words_dict:
		# print dictonary['sender']
		# print dictonary['words']
		try:
				matrix = count_vect.fit_transform(dictonary['words'])
				freqs = [[word, matrix.getcol(idx).sum()] for word, idx in count_vect.vocabulary_.items()]
				keywords = sorted(freqs, key = lambda x: -x[1])
				# print 'Nick:', dictonary['sender']
				total_freq = 0.0
				for freq_tuple in keywords:
					total_freq+=freq_tuple[1]
				# print total_freq
				
				for freq_tuple in keywords:
					freq_tuple.append(round(freq_tuple[1]/float(total_freq),5))
				user_keyword_freq_dict.append({'nick':dictonary['sender'], 'keywords': keywords })

				# print 'Keywords: (Format : [<word>, <frequency>, <normalised_score>])'
				# print keywords
				# print "\n"
		except ValueError:
				pass
	
	# print user_keyword_freq_dict
	# print dataForNick(user_keyword_freq_dict, 'BluesKaj', 0.01)
	for data in user_keyword_freq_dict:
		keywords, normal_scores = dataForNick(user_keyword_freq_dict, data['nick'], 0.01, 100)
		# print "Nick:", data['nick']
		# print "Keywords with normalised score > 0.01\n", keywords
		# print "Their Normal scores\n", normal_scores
		# print "\n"
		if keywords:
			keywords_filtered.append({'nick':data['nick'],'keywords': keywords})
			
	# print "KEYWORDS!"
	# print keywords_filtered
	# print "DICT"
	# print user_keyword_freq_dict
	print str(startingMonth)+"\t"+str(no_messages)+"\t"+str(len(user_words_dict))
	return keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words