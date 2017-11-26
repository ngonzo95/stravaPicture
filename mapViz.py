import folium
from colour import Color
import collections
import json

class RunMap:
	"""docstring for RunMap"""
	#initilize the feilds for generating the map. The only needed argument is the starting point.
	#optional fields include map type and the number of runs the map display. you can also specify
	#a specific colorGradient which is a list of different colors of size numRuns, the oldest run
	#will use the color at index 0
	def __init__(self, numRuns, startPoint=[44.9501,-93.2701] ,
		mapType='https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
		attr='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
		colorGrad = None):

		#Set the memeber variables
		self._mapType = mapType
		self._attr = attr
		self._startPoint = startPoint
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
		mapViz = folium.Map(location=self._startPoint,
			zoom_start=12,
			tiles= self._mapType,
			attr= self._attr)

		#mapViz.create_map(path='map.html', template='runHTMLTemplate.html')

		for i in range(len(self._runList)):
			runViz = folium.PolyLine(locations=self._runList[i], color=self._colors[i].hex, opacity=0.4)
			runViz.add_to(mapViz)


		#save the map to the maps file
		mapViz.save('templates/map.html')


	"""Adds a run to the map. This function takes in a list of gps points """
	def addRun(self,gps):
		#if we have to many runs then remove the oldest run from this list (which is the first one)
		if len(self._runList) == self._numRuns:
			self._runList.popleft()

		#add the run to the list
		self._runList.append(gps)

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

			self._runList = collections.deque(savedQueue)
			return lastRun
        #If the load fails makes sure the queue is empty and we return 0
		except Exception, e:
			self._runList = collections.deque()
			return 0


			lastRun, runIDs = client.getLastNRunIDs(numRuns)
			runGPS = getGPS(client, runIDs)


		

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