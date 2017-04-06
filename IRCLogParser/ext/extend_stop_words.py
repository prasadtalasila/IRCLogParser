#this is a list of custom stop words which are not included in normal english conversation but are trivial in the tech-world
#also inlcludes slangs
'''
	The list has to be all in lowercase
	Use the function to concert them all : words = map(lambda x:x.lower(),words) 
'''

words = ['fail', 'connect', 'failed', 'infact', 'later', 'guys', 'jesus', 'monday', 'tuesday', 'wednesday' ,'thursday', 'friday', 'saturday', 'sunday']
slangs = ['btw', 'ok', '2f4u', '4yeo', 'aamof', 'ack', 'afaik', 'afair', 'afk', 'aka', 'b2k', 'btt', 'btw', 'b/c', 'c&p', 'cu', 'cys', 'diy', 'eobd', 'eod', 'eom', 'eot', 'faq', 'fack', 'fka', 'fwiw', 'fyi', 'ftw', 'hf', 'hth', 'idk', 'iirc', 'imho', 'imo', 'imnsho', 'iow', 'itt', 'lol', 'mmw', 'n/a', 'nan', 'nntr', 'noob', 'noyb', 'nrn', 'omg', 'op', 'ot', 'otoh', 'pebkac', 'pov', 'rotfl', 'rsvp', 'rtfm', 'scnr', 'sflr', 'spoc', 'tba', 'tbc', 'tia', 'tgif', 'thx', 'tq', 'tyvm', 'tyt', 'ttyl', 'woot', 'wfm', 'wrt', 'wth', 'wtf', 'ymmd', 'ymmv', 'yam', 'hehe']