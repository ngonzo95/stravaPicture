import folium
from colour import Color
import collections
import json
from math import radians, cos, sin, asin, sqrt

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
		self._mapType = mapType
		self._attr = attr
		self._startPoints = startPoint
		self._numRuns = numRuns

		#Create a list that will hold our runs
		self._runList = collections.deque()

		#If we were not given a color gradient generate our own
		if colorGrad == None:
			startColor = Color("#0D1D3B")
			colorGrad = list(startColor.range_to(Color("#FFA13D"), numRuns))

		self._colors = colorGrad

	"""Renders the map and saves the html file"""
	def genMap(self):
		#Create a map for each of the starting points
		for j in range(len(self._startPoints)):
			mapViz = folium.Map(location=self._startPoints[j],
				zoom_start=12,
				tiles= self._mapType,
				attr= self._attr)

			#mapViz.create_map(path='map.html', template='runHTMLTemplate.html')

			for i in range(len(self._runList)):
				runViz = folium.PolyLine(locations=self._runList[i], color=self._colors[i].hex, opacity=0.4)
				runViz.add_to(mapViz)


			#save the map to the map file
			mapViz.save('templates/maps/map'+ str(j) +'.html')


	"""Adds a run to the map. This function takes in a list of gps points """
	def addRun(self,gps):
		#if we have to many runs then remove the oldest run from this list (which is the first one)
		if len(self._runList) == self._numRuns:
			self._runList.popleft()

		#add the run to the list
		self._runList.append(gps)

		#Figure out if we need to add a new starting point for this run or if it will fit in 
		#an existing map
		self._checkPointOnMap(gps[0])

	"""Save all the file information by saving the runlist queue and the
	   time of the last run."""
	def saveRuns(self, lastRun):
		with open ('runSave.json','w') as outfile:
			json.dump((lastRun, list(self._runList)), outfile)

	"""Load from file and return the time of the last run. If we get an error
	   while loading the queue will revert to empty and return 0."""
	def loadRuns(self):
		#Try to load from the file 
		try:
			with open('runSave.json') as saveFile:    
				lastRun, savedQueue = json.load(saveFile)

			#Go through the run list to load starting points
			for run in savedQueue:
				self._checkPointOnMap(run[0])

			self._runList = collections.deque(savedQueue)

			return lastRun
        
        #If the load fails makes sure the queue is empty and we return 0
		except Exception, e:
			print e
			self._runList = collections.deque()
			return 0


			lastRun, runIDs = client.getLastNRunIDs(numRuns)
			runGPS = getGPS(client, runIDs)


	"""Gets the number of maps the map viz will create at this point"""
	def numMaps(self):
		return len(self._startPoints)


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

	"""Checks if this point is visable in a map and if it is not it adds it as a starting point
	   of a new map"""

	def _checkPointOnMap(self, point):
		addPoint = True
		for gpsPoint in self._startPoints:
			if self._distBetween(gpsPoint, point) < 100:
				addPoint = False
				break

		#If we did not return by this point then this point does not fit in a map and we must 
		#add one for it
		if addPoint:
			self._startPoints.append(point)


		

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