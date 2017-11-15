import urllib2
import json
import time

class StravaAPI:
	"""This class acts as an interface between the rest of the program and the 
	strava web api. To initalize pass a string provides a path to get the a 
	token which is a valid strava access token in plain text with nothing but 
	the token itself """
	def __init__(self, tokenFileName):
		#Save the token from the given file and then close the file
		tokenFile = open(tokenFileName, 'r')
		self._token = tokenFile.read()
		tokenFile.close()

	#Deals with all of the sending and reciveing of the url calls to stava
	#This function takes a url and returns a dictonary representing the
	#returned json object
	def _sendRequest(self, url):
		#Create the basic request
		req = urllib2.Request(url)

		#add the needed authentification header
		tokenString = 'access_token ' + self._token
		req.add_header('Authorization', tokenString)

		res = None
		#Load the url and return the json object
		try:
			res = urllib2.urlopen(req)
		
		#If we cannot load the url then return the empty string
		#and print the error
		except Exception, e:
			print str(e)
			return []

		#return the resulting json object as a dictonary
		return json.loads(res.read())

	""" This is a private function that helps us test different things with the api """
	def _getRunIDs(self):
		#Get the activities from the strava api
		activities = self._sendRequest('https://www.strava.com/api/v3/activities')

		print self._getTime(activities[8])

		runIDs = []
		self._addRunIDsToList(activities,runIDs)

	def _addRunIDsToList(self, activities, runIDs):
		for act in activities:
			#Filter out the list so that we only get the runs with gps signals
			if (act['type'] == "Run" and 'start_latlng' in act and act['start_latlng'] != None):
				runIDs.append(act['id'])

	#This is a helper function that gets the timestamp for an activity 
	def _getTime(self, activity):
		#Get the utc time from the activity formated in the way strava likes it
		stravaTime = activity['start_date']

		#Convert it to Epoch time so that we can use it in queries
		#2017-11-09T16:31:00Z
		pattern = '%Y-%m-%dT%H:%M:%SZ'
		
		#Convert into epoch Time
		epochTime = int(time.mktime(time.strptime(stravaTime, pattern)))

		return epochTime

	#This is a helper function which takes a baseURL which we will query strava with
	#and reads until we have read all possible pages or reach a certin number of runs
	def _getRunIDsFromBaseURL(self, baseURL, lastRunTime, maxRuns=100):
		#Initilize all of the variables
		pageNum = 1
		runIDs = []
		timeStamp = ''

		#Grab the first page
		url = baseURL + str(pageNum)
		activities = self._sendRequest(url) 
		
		#If the page returns empty there are no runs to be taken
		if activities == []:
			return(lastRunTime,[])

		#Get the time of the latest activity
		timeStamp = self._getTime(activities[0])

		#continue until the page we query from strava is empty
		while activities:
			#Add the run ids to the list 
			self._addRunIDsToList(activities,runIDs)

			#Increment the page number
			pageNum += 1

			#Create the url to query and query it
			url = baseURL + str(pageNum)
			activities = self._sendRequest(url)

			#If we hit the max before we read all the pages end
			if len(runIDs) > maxRuns:
				#Clean up the array so we only have the max
				runIDs = runIDs[:maxRuns]
				break

			#if there are alot of pages that do not have runs exit
			#so we dont accidentally overload the api
			if pageNum > (maxRuns/3):
				break

		return(timeStamp,runIDs)


	"""This function gets the last numRuns runIDS a user has done from the strava api.
	This function returns a tuple which includes the timestamp of the latest activity done"""
	def getLastNRunIDs(self, numRuns):
		#This is the base url that will get all the activities from a certin page
		baseURL = 'https://www.strava.com/api/v3/activities?page='

		return self._getRunIDsFromBaseURL(baseURL, 0, maxRuns= numRuns)

	"""Gets the all the runs since a given time. Optional argument to set a maximum on
	the number of runs you want"""
	def getLatestRuns(self, lastRunTime):
		#Create base URL and initalize parameters
		baseURL = 'https://www.strava.com/api/v3/activities?after=' +str(lastRunTime) + '&page='
		
		return self._getRunIDsFromBaseURL(baseURL,lastRunTime)



	""" This function takes in a run id and returns the runs gps information as
	a list of gps position lists"""
	def getGPSFromID(self, runID):
		url = 'https://www.strava.com/api/v3/activities/' + str(runID) + '/streams/latlng'
		runData = self._sendRequest(url)

		#Extract the latlong data from the run data. it should always be the first but just in case
		#we look until we find it
		latLong = []
		for data in runData:
			if data['type'] == 'latlng':
				latLong = data['data']
				#once we find the data we want we can stop looking
				break

		return latLong



		
		

#Basic script to show that class functions work as expected
def main():
	client = StravaAPI('/Users/Nick/Documents/stravaProject/stravaPicture/token.txt')
	timeStamp, runIDs = client.getLastNRunIDs(100)

	#runIDs = client._getRunIDs()
	#timeStamp, runIDs = client.getLatestRuns(1507575398)

	print timeStamp
	print len(runIDs)
	
	# gpsData = []
	# for ID in runIDs:
	# 	gpsData.append(client.getGPSFromID(ID))

	# with open ('gps.json','w') as outfile:
	# 	json.dump(gpsData, outfile)


if __name__ == '__main__':
	main()