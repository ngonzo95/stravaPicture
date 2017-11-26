from stravaAPI import StravaAPI
from mapViz import RunMap
import time
import jinja2
#import threading

#This is the function that runs the strava picture program
def main():
	#initilization
	client = StravaAPI("token.txt")
	numRuns = 30
	m = RunMap(numRuns, startPoint=[[44.9501,-93.2701],[42.352190,-71.078996]])

	#In the case where there is no base file and we cannot connect to
	#the strava api we will keep trying to initilize 
	lastRun = initInfo(client,m,numRuns)
	while lastRun == 0:
		lastRun = initInfo(client,m,numRuns)
		#Try every 5 minutes
		time.sleep(300)
		
	#generate the map for the first time
	m.saveRuns(lastRun)
	m.genMap()
	genHTML()
	print "First map generated"

	#Now we just update and save forever
	while True:
		#Update every 30 mins
		time.sleep(1800)
		lastRun = updateInfo(client,m,lastRun)
		m.saveRuns(lastRun)
		m.genMap()
		genHTML()
		print "New map generated"



	#TODO use threads to allow us to do other things while we are waiting
	#Update the map every 30 minutes
	#threading.Timer(1800, updateInfo(client,m,runIDs,runGPS,lastRun))

	#Save progress every day
	#threading.Timer(864000, saveInfo(runIDs,runGPS,lastRun))

def updateInfo(client,m,lastRun):
	print "updating info"
	#Get the last couple runs
	lastRun, newRunIDs = client.getLatestRuns(lastRun)

	addRunIDsToMap(client, m, newRunIDs)

	return lastRun


def initInfo(client,m,numRuns):
	print "initilizing info"
	#Try to load runs from file
	print "Trying to load runs from save"
	lastRun = m.loadRuns()
    
    #If the load failed get runs from the API
	if lastRun == 0:
		print "Load Failed Calling the StravaAPI"
		lastRun, runIDs = client.getLastNRunIDs(numRuns)
		addRunIDsToMap(client, m, runIDs)
	else:
		print "Load Succeded"

	return lastRun

def addRunIDsToMap(client,m,runIDs):
	#use the strava api to add runs to the map based on runIDs
	for runID in reversed(runIDs):
		run = client.getGPSFromID(runID)
		m.addRun(run)

def genHTML():
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates")
	templateEnv = jinja2.Environment(loader=templateLoader)
	TEMPLATE_FILE = "template.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	outputText = template.render({'baseMap':'maps/map0.html','maps':[{'href':'index1.html', 'caption': 'min'}, {'href':'index2.html', 'caption': 'bos'}]}) # this is where to put args to the template renderer

	with open("views/index1.html", "wb") as fh:
		fh.write(outputText)		

	outputText = template.render({'baseMap':'maps/map1.html','maps':[{'href':'index1.html', 'caption': 'min'}, {'href':'index2.html', 'caption': 'bos'}]}) # this is where to put args to the template renderer

	with open("views/index2.html", "wb") as fh:
		fh.write(outputText)


if __name__ == '__main__':
	main()