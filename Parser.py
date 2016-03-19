import lib.NickChangeGraph as NCG 
import lib.MessageTimeGraph as MTG
import lib.MessageNumberGraph as MNG
import lib.MessageNumberBinsCSV as MNBC
import lib.AggregateGraph as AG
import lib.ChannelsOfNickGraph as CNG
import lib.createKeyWords as CKW

def createNickChangesGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	NCG.createNickChangesGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)

def createMessageTimeGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	MTG.createMessageTimeGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)

def createMessageNumberGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	MNG.createMessageNumberGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)

def createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	MNBC.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingMonth, endingMonth)
	
def createAggregateGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	AG.createAggregateGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)

def createChannelsOfNickGraph(log_directory, output_directory, startingMonth, endingMonth):
	CNG.createChannelsOfNickGraph(log_directory, output_directory, startingMonth, endingMonth)

def createKeyWords(log_directory, channel_name, output_directory, startingMonth, endingMonth):
	CKW.createKeyWords(log_directory, channel_name, output_directory, startingMonth, endingMonth)
