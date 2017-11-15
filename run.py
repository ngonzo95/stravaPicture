from stravaAPI import StravaAPI
from mapViz import RunMap
import time
import json
#import threading

#This is the function that runs the strava picture program
def main():
	#initilization
	runIDs = []
	runGPS = []
	client = StravaAPI("token.txt")
	numRuns = 30
	m = RunMap([44.9501,-93.2701],numRuns)

	#In the case where there is no base file and we cannot connect to
	#the strava api we will keep trying to initilize 
	lastRun, runIDs, runGPS = initInfo(client,m,numRuns)
	while lastRun == 0:
		lastRun, runIDs, runGPS = initInfo(client,m,numRuns)
		#Try every 5 minutes
		time.sleep(300)
		
	#generate the map for the first time
	m.genMap()
	print "First map generated"

	#Now we just update and save forever
	while True:
		#Update every 30 mins
		time.sleep(1800)
		lastRun, runIDs, runGPS = updateInfo(client,m,runIDs,runGPS,lastRun)
		saveInfo(runIDs,runGPS,lastRun)
		m.genMap()



	#TODO use threads to allow us to do other things while we are waiting
	#Update the map every 30 minutes
	#threading.Timer(1800, updateInfo(client,m,runIDs,runGPS,lastRun))

	#Save progress every day
	#threading.Timer(864000, saveInfo(runIDs,runGPS,lastRun))

def updateInfo(client,m,runIDs,runGPS,lastRun,numRuns):
	print "updating info"
	#Get the last couple runs
	lastRun, newRunIDs = client.getLatestRuns(lastRun)

	#get the gps of these runs and add them to the map
	newRunGPS = []
	for runID in newRunIDs:
		run = client.getGPSFromID(runID)
		m.addRun(run)
		newRunGPS.append(newRunGPS)

	#Add the new run to the old one
	runIDs = newRunIDs + runIDs
	runGPS = newRunIDs + runGPS

	#get rid of the oldest runs
	runIDs = runIDs[:numRuns]
	runGPS = runGPS[:numRuns]

	return (lastRun, runIDs, runGPS)


def initInfo(client,m,numRuns):
	print "initilizing info"
	#First we want to try and load a previous load file. If we get an exception
	#Then we just throw it all out and start from scratch
	lastRun = 0
	runIDs = []
	runGPS = []

	try:
		print "loading from save"
		lastRun, runIDs, runGPS = loadInfo()
		print "load succeded"
	#if something goes wrong while reading the file then just load everthing from the
	#webiste
	except Exception, e:
		print "load failed. requesting API"
		lastRun, runIDs = client.getLastNRunIDs(numRuns)
		runGPS = getGPS(client, runIDs)

		if lastRun != 0:
			#Save the info for the first time so we have it for later
			saveInfo(runIDs, runGPS, lastRun)

	#add the runs to the map with the first one being added on last
	for run in reversed(runGPS):
		m.addRun(run)

	return (lastRun, runIDs, runGPS)

def saveInfo(runIDs,runGPS,lastRun):
	print "saving Info"
	#Create a dictonary with all of the required information
	saveDict = {}
	saveDict['runIDs'] = runIDs
	saveDict['runGPS'] = runGPS
	saveDict['lastRun'] = lastRun
	
	with open ('runSave.json','w') as outfile:
		json.dump(saveDict, outfile)

def loadInfo():
	saveDict = {}
	with open('runSave.json') as saveFile:    
		saveDict = json.load(saveFile)

	return(saveDict['lastRun'], saveDict['runIDs'], saveDict['runGPS'] )

def getGPS(client,runIDs):
	runGPS = []
	#use the strava api to get run ids
	for runID in runIDs:
		runGPS.append(client.getGPSFromID(runID))

	return runGPS
		



if __name__ == '__main__':
	main()