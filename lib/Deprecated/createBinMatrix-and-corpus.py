import createKeyWords as CKW

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/"
startingDate = 1
startingMonth = 1
endingDate = 4
endingMonth = 2


user_list = []
keyword_list = []
keyword_dict_list, user_keyword_freq_dict = CKW.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)

for dictionary in keyword_dict_list:
	user_list.append(dictionary['nick'])
	keyword_list = list(set(keyword_list + dictionary['keywords']))

keyword_user_binary_matrix = [[0 for i in xrange(len(user_list))] for x in xrange(len(keyword_list))]

# print user_list
# print keyword_list
# print keyword_user_binary_matrix

for user in user_list:
	key_words_for_users = filter(lambda keywords_user: keywords_user['nick'] == user, keyword_dict_list)[0]['keywords']
	for word in key_words_for_users:
		keyword_user_binary_matrix[keyword_list.index(word)][user_list.index(user)] = 1

print user_list, "\n"
print keyword_list, "\n"
print keyword_user_binary_matrix


# from nltk.corpus.reader import CategorizedPlaintextCorpusReader
# reader = CategorizedPlaintextCorpusReader('/home/rohan/parser_files/2013/01/01', r'\#.*\.txt', cat_pattern = r'\#(\w+).*\.txt')
# print reader.categories()
# print reader.fileids(categories=['ubuntu'])