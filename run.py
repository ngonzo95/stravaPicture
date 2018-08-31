from stravaAPI import StravaAPI
from mapViz import RunMap
from S3UploadViews import upload_views_to_s3
import time
import jinja2
import dill
import pickle
#import threading

#This is the function that runs the strava picture program
def main():
	print "Starting time, ", time.asctime(time.localtime())
	#initilization
	client = StravaAPI("token.txt")
	numRuns = 60

	#In the case where there is no base file and we cannot connect to
	#the strava api we will keep trying to initilize 
	lastRun, m = initInfo(client, numRuns)
	while lastRun == 0:
		lastRun, m = initInfo(client, numRuns)
		#Try every 5 minutes
		time.sleep(300)
		
	#generate the map for the first time
	saveInfo(lastRun,m)
	m.genMap()
	genHTML(m)
	upload_views_to_s3()
	print "First map generated, ", time.asctime(time.localtime())

	#Now we just update and save forever
	while True:
		#Update every 30 mins
		time.sleep(3600)
		lastRun = updateInfo(client,m,lastRun)

		saveInfo(lastRun,m)
		m.genMap()
		genHTML(m)
		upload_views_to_s3()
		print "New map generated, ", time.asctime(time.localtime())
		print "Last run saved was at: ", lastRun


def updateInfo(client,m,lastRun):
	print "updating info"
	#Get the last couple runs
	lastRun, newRunIDs = client.getLatestRuns(lastRun)

	addRunIDsToMap(client, m, newRunIDs)

	return lastRun


def initInfo(client, numRuns):
	print "initilizing info"
	#Try to load runs from file
	print "Trying to load runs from save"
	try:
		lastRun, runMap = pickle.load( open( "runSave_1V_1.p", "rb" ) )
		print "Load Succeded"

		return lastRun, runMap
	
	#If the load fails Then we quiery the StravaAPI and make our own new map
	except Exception, e:
		print "exception in run.py: ", e
		runMap = RunMap(numRuns)

		print "Load Failed Calling the StravaAPI"
		lastRun, runIDs = client.getLastNRunIDs(3*numRuns)
		addRunIDsToMap(client, runMap, runIDs)

		return lastRun, runMap
	

def addRunIDsToMap(client,m,runIDs):
	#use the strava api to add runs to the map based on runIDs
	for runID in reversed(runIDs):
		run = client.getGPSFromID(runID)
		m.addRun(run)

def genHTML(m):
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates")
	templateEnv = jinja2.Environment(loader=templateLoader)
	TEMPLATE_FILE = "template.html"
	template = templateEnv.get_template( TEMPLATE_FILE )

	#Now render each map with its own index file
	renderDict = m.getMapDropdownDict()

	#render all of the area maps plus the worldMap
	for i in range(m.numMaps()+1):
		renderDict['baseMap'] = 'maps/map' + str(i) + '.html'

		outputText = template.render(renderDict)
		fileName = 'views/index' + str(i) + '.html'

		with open(fileName, "wb") as fh:
			fh.write(outputText)		

def saveInfo(lastRun,m):
	pickle.dump( (lastRun,m), open( "runSave_1V_1.p", "wb" ) )
	pickle.dump((lastRun,m.rawSave()), open( "raw_runSave.p", "wb" ))

if __name__ == '__main__':
	main()
