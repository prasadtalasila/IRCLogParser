OUT_DIR="/home/rohan/parser_files/Output"
IN_DIR="/home/rohan/parser_files/YearlyLogFiles/"

METHODS_TO_RUN="nickChange
messageTime
messageNumber
messageNumberBins
degNodeNumberCSV
aggregate
keyWords
responseTime
convLenRefresh"

CONSIDERED_CHANNELS="#kubuntu-devel
#kubuntu
"

rm -rf $OUT_DIR"/LOGS"
mkdir $OUT_DIR"/LOGS"


for CHANNEL in $CONSIDERED_CHANNELS
do
	for METHOD in $METHODS_TO_RUN
	do
		echo "\n\n========" "["$CHANNEL"]" $METHOD "========"
		
		for YEAR in "2013" "2014" "2015"
		do
			echo "\n["$YEAR"]"
			
			for MONTH in "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12"
			do
				echo -n $MONTH" "
				#RUN THE FUNCTION
				python module.py $METHOD \
					-c=$CHANNEL \
					-i=$IN_DIR"/"$YEAR"/" \
					-o=$OUT_DIR"/"$CHANNEL"/"$METHOD"/"$YEAR"/"$MONTH"/" \
					-f="1-"$MONTH \
					-t="31-"$MONTH \
					> $OUT_DIR"/LOGS/"$METHOD"_"$YEAR"_"$MONTH".txt" 
			done
		done
	done
done


'''
	====================================================
	NOTE:
	----------------------------------------------------
	channel-nick script runs over all channels 
	unlike the channel specific scripts dealt with above
	hence it is run seperately below
	====================================================
'''
# MONTH="1"
# YEAR="2013"
# python module.py "channel-nick" \
# 					-i=$IN_DIR$YEAR"/" \
# 					-o=$OUT_DIR"/"$CHANNEL"/channel-nick/"$YEAR"/"$MONTH"/" \
# 					-f="1-"$MONTH \
# 					-t="31-"$MONTH 