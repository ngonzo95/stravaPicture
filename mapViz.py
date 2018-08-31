import folium
from colour import Color
import collections
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
from areaMap import AreaMap
from worldMap import WorldMap

class RunMap:
	"""docstring for RunMap"""
	#initilize the feilds for generating the map. The only needed argument is the starting point.
	#optional fields include map type and the number of runs the map display. you can also specify
	#a specific colorGradient which is a list of different colors of size numRuns, the oldest run
	#will use the color at index 0
	def __init__(self, numRuns, startPoint=[] ,
		mapType='https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
		attr='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
		colorGrad = None):

		#Set the memeber variables
		self._baseMap = mapType
		self._attr = attr
		self._numRuns = numRuns
		self._nextMapID = 0

		#If we were not given a color gradient generate our own
		if colorGrad == None:
			startColor = Color(rgb=[0.05,0.11,1])
			colorGrad = list(startColor.range_to(Color(rgb=[1,0,0.35]), numRuns))

		self._colors = colorGrad

		#Create the list of area maps
		self._areaMaps = []

		#Create the worldMap
		self._worldMap = WorldMap(self._nextMapID, [39.8333,-98.58333], self._baseMap, self._attr)
		self._nextMapID += 1

		#For all the starting points listed create a map
		for i in range(len(startPoint)):
			areaMap = self._CreateNewMap(startPoint[i])

	"""Renders the map and saves the html file"""
	def genMap(self):
		#Create a map for each of the starting points
		for areaMap in self._areaMaps:
			areaMap.genMap()

		self._worldMap.genMap()
			


	"""Adds a run to the map. This function takes in a list of gps points """
	def addRun(self,gps):
		#Try to add it to existing maps
		runAdded = False
		for areaMap in self._areaMaps:
			#If we can add the run to one of the existing maps do it
			if self._distBetween(gps[0], areaMap.startPoint) < 100:
				areaMap.addRun(gps)
				runAdded = True

		#If the run was not added to any maps then create an new area map and add it to that
		if not runAdded:
			newMap = self._createNewMap(gps[0])
			newMap.addRun(gps)
			self._worldMap.addArea(newMap.startPoint, self._getCaption(newMap.startPoint), newMap.mapID)

	"""Gets the number of maps the map viz will create at this point"""
	def numMaps(self):
		return len(self._areaMaps)

	"""Returns a map that is uses for creating the drop down options"""
	def getMapDropdownDict(self):
		#First we can make the maps list since that will be the same in all cases
		#todo get mapID startPoint Pairs
		mapList = [{'href':'index0.html','caption':'USA Map'}]


		for areaMap in self._areaMaps:
			mapDict = {}
			mapDict['href'] = 'index' + str(areaMap.mapID) + '.html'
			mapDict['caption'] = self._getCaption(areaMap.startPoint)
			mapList.append(mapDict)

		return {'maps': mapList}

	def rawSave(self):
		runsToSave = []

		for aMap in self._areaMaps:
			runsFromArea = aMap.getRunsToSave()
			for run in runsFromArea:
				runsToSave.append(run)

		return runsToSave


	"""Estimates distance between two gps points in km taken from stack
	   exchange:"""

	def _distBetween(self,p1,p2):
		lat1 = p1[0]
		lon1 = p1[1]
		lat2 = p2[0]
		lon2 = p2[1]
		# convert decimal degrees to radians 
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
		# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		# Radius of earth in kilometers is 6371
		km = 6371* c
		return km

	def _getCaption(self, point):
		
		#Try to get a city or town name, if not possible just return map
		try:
			#Get the location information from geolocator
			geolocator = Nominatim(user_agent="strava_picture_sarah")
			pointList = point
			pointStr = str(pointList[0]) + ', ' + str(pointList[1])
			location = geolocator.reverse(pointStr, timeout=10)
			possibleTitles= ['city', 'town', 'hamlet', 'village']

			for title in possibleTitles:
				if title in location.raw['address']:
					return location.raw['address'][title]

			print "Weird location recived"
			print location.raw
			return "Map"
		except Exception, e:
			print "geoLocator threw exception: ", e
			return "Map"

	def _createNewMap(self, startPoint):
		newMap = AreaMap(self._nextMapID, self._numRuns, startPoint, self._baseMap, self._attr, self._colors)
		self._nextMapID += 1
		self._areaMaps.append(newMap)

		#Return the map incase they want to add things to it
		return newMap


#A sample script to run to test the file
def main():
	#We only want to import json for testing
	import json

	gps =[]
	#get the path data from an example json file
	with open('gps.json') as data_file:    
		gps = json.load(data_file)

	#Create the base map centered on the most recent run
	m = RunMap(gps[0][0],100)

	#add each of the runs with a different color
	#This list is reversed so that the newest runs are added lasy
	#and therefore on top
	for run in reversed(gps):
		m.addRun(run)

	#same the html of the map so we can look at it
	m.genMap()





if __name__ == '__main__':
	main()