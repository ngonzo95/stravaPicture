import folium
from colour import Color
import collections

class RunMap:
	"""docstring for RunMap"""
	#initilize the feilds for generating the map. The only needed argument is the starting point.
	#optional fields include map type and the number of runs the map display. you can also specify
	#a specific colorGradient which is a list of different colors of size numRuns, the oldest run
	#will use the color at index 0
	def __init__(self, startPoint, numRuns,
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
			zoom_start=13,
			tiles= self._mapType,
			attr= self._attr)

		for i in range(len(self._runList)):
			runViz = folium.PolyLine(locations=self._runList[i], color=self._colors[i].hex, opacity=0.4)
			runViz.add_to(mapViz)


		#save it to a temporary html
		mapViz.save('index.temp.html')

		#add the auto refresh line to the html file
		with open('index.temp.html', 'r') as infile:
			with open('index.html', 'w') as outfile:
				counter = 0
				for line in infile:
					if counter == 2:
						#This makes it some the html will automaticall refresh every 30 mins
						outfile.write('<META HTTP-EQUIV="refresh" CONTENT="1800"/> \n')
					outfile.write(line)
					counter += 1

	"""Adds a run to the map. This function takes in a list of gps points """
	def addRun(self,gps):
		#if we have to many runs then remove the oldest run from this list (which is the first one)
		if len(self._runList) == self._numRuns:
			self._runList.popleft()

		#add the run to the list
		self._runList.append(gps)


		

#A sample script to run to test the file
def main():
	#We only want to import json for testing
	import json

	gps =[]
	#get the path data from an example json file
	with open('gps.json') as data_file:    
		gps = json.load(data_file)

	#Create the base map centered on the most recent run
	m = RunMap(gps[0][0],10)

	#add each of the runs with a different color
	for i in range(len(gps)):
		m.addRun(gps[i])

	#same the html of the map so we can look at it
	m.genMap()





if __name__ == '__main__':
	main()