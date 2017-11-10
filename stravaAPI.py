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

	""" This function quieries the strava api to find out all the activities they
	have done and then selects only the runs which have gps values associated with
	them. It then returns all of thoes ids in a list """
	def getRunIDs(self):
		#Get the activities from the strava api
		activities = self._sendRequest('https://www.strava.com/api/v3/activities')

		
		runIDs = []
		for act in activities:
			#Filter out the list so that we only get the runs with gps signals
			if (act['type'] == "Run" and 'start_latlng' in act and act['start_latlng'] != None):
				runIDs.append(act['id'])

		return runIDs

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
	runIDs = client.getRunIDs()
	
	gpsData = []
	for ID in runIDs:
		gpsData.append(client.getGPSFromID(ID))

	with open ('gps.json','w') as outfile:
		json.dump(gpsData, outfile)


if __name__ == '__main__':
	main()