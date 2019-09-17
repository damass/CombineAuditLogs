##################################################################################################
#
#	Name		: combineAuditLogs.py
#	Creation Date 	: 2019-08-11
#	Version 	: 1.1 
#	
#	Requires: Python3
#			  Dynatrace Managed v158+
#
#	Use : Place combineAuditLogs.py in the same directory as al the audit.user.0.0.log 
#		 and run the script. It will create a single full.audit.user.0.0.log file that 
#		 combines all the individual node log files into one. 
#
#	Purpose : Creates a single audit user log file from multiple log files from each Dynatrace
#			  Managed Node. 
#
####################################################################################################

import logging
from datetime import datetime 
import time 
import json 

strDateTime = str(time.strftime("%Y%m%d_%H%M%S",time.localtime())) #date&time for output files

#set up logging 
logFileName = "combine-audit-logs-log."+strDateTime+".log"
#logging.basicConfig(filename=logFileName,level=logging.DEBUG)
logging.basicConfig(filename=logFileName,level=logging.INFO)
logging.info('Log File Open')


#Array that contains each node's log file name. Add additional items for each new Dynatrace Node 
individualAuditLogFiles = ["ServerNode001 - audit.user.0.0.log","ServerNode002 - audit.user.0.0.log","ServerNode003 - audit.user.0.0.log"]
fullEpochLogMessageDict = dict()
fullDateLogMessageDict = dict()
combinedAuditLogFile = "full.audit.user.log"


for inputFileName in individualAuditLogFiles: 
	logging.debug(inputFileName + " is being processed")
	with open(inputFileName) as inputFile: #Open & Read in each line of the Audit User Log
		logging.debug(inputFileName + " is now open")
		#begin main loop
		for line in inputFile:
			linePieces = line.strip()
			logging.debug('Splitting Line')
			linePieces = linePieces.split(" ", 3)
			
			logging.debug('Try to catch older log messages that were not JSON Formatted')
			try:
				logMessageJSONDict = json.loads(linePieces[3])
				strTimeStamp = str(logMessageJSONDict['timestamp'])
			
			
				if not strTimeStamp.startswith(('2018','2019')):
					updatedInfo = {logMessageJSONDict['timestamp']:line}
					logging.debug(updatedInfo)
					fullEpochLogMessageDict.update(updatedInfo)
				else:
					updatedInfo = {logMessageJSONDict['timestamp']:line}
					logging.debug(updatedInfo)
					fullDateLogMessageDict.update(updatedInfo)				

			except ValueError as e:
				#catch exception thrown by json.loads() method 
				logging.debug('Line not JSON Formatted')
				continue 	

#opening output file 
outputCombinedAuditLogFile = open(combinedAuditLogFile, "a")

#Print out Dictionary Values 
logging.info('Start Printing Date Keys')
for key in sorted(fullDateLogMessageDict.keys()): 
	 logging.debug(fullDateLogMessageDict[key])
	 outputCombinedAuditLogFile.write(fullDateLogMessageDict[key])
logging.info('Stop Printing Date Keys')

logging.info('Start Printing Epoch Keys')
for key in sorted(fullEpochLogMessageDict.keys()): 
	 logging.debug(fullEpochLogMessageDict[key])
	 outputCombinedAuditLogFile.write(fullEpochLogMessageDict[key])
logging.info('Stop Printing Epoch Keys')

#closing output file 
outputCombinedAuditLogFile.close()

logging.info('Script Completed Successfully')
			