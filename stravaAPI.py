import urllib2
import json

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

		#Load the url and return the json object
		res = urllib2.urlopen(req)

		#TODO deal with failed requests

		#return the resulting json object as a dictonary
		return json.loads(res.read())

	""" This is a private function that helps us test different things with the api """
	def _getRunIDs(self):
		#Get the activities from the strava api
		activities = self._sendRequest('https://www.strava.com/api/v3/activities')

		print activities[0]

		runIDs = []
		self._addRunIDsToList(activities,runIDs)

	def _addRunIDsToList(self, activities, runIDs):
		for act in activities:
			#Filter out the list so that we only get the runs with gps signals
			if (act['type'] == "Run" and 'start_latlng' in act and act['start_latlng'] != None):
				runIDs.append(act['id'])



	"""This function gets the last numRuns runIDS a user has done from the strava api.
	This function returns a tuple which includes the timestamp of the latest activity done"""
	def getLastNRunIDs(self, numRuns):
		#This is the base url that will get all the activities from a certin page
		baseURL = 'https://www.strava.com/api/v3/activities?page='

		runIDs = []

		#pages numbers start at 1
		pageNum = 1


		#Go through all of the pages until we have the desired number of runs
		while len(runIDs) < numRuns:
			#Create the url to query and query it
			url = baseURL + str(pageNum)
			activities = self._sendRequest(url)

			#Add the run ids to the list 
			self._addRunIDsToList(activities,runIDs)

			#If this is the first page we want to 
			#Increment the page number
			pageNum += 1

			#Limit the number of pages we can look at so we dont go on forever
			#if they dont have enough runs
			if pageNum > (numRuns/3):
				break

		#We may get more runs than we need so only return the amount they asked for
		return runIDs[:numRuns]

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
	#runIDs = client.getLastNRunIDs(50)

	#runIDs = client.getRunIDs()
	
	# gpsData = []
	# for ID in runIDs:
	# 	gpsData.append(client.getGPSFromID(ID))

	# with open ('gps.json','w') as outfile:
	# 	json.dump(gpsData, outfile)


if __name__ == '__main__':
	main()