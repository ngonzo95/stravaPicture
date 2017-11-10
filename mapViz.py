import folium
from colour import Color

class RunMap:
	"""docstring for RunMap"""
	#create the map which we will be using 
	def __init__(self, startPoint):
		self._map = folium.Map(location=startPoint,
			zoom_start=13,
			tiles= 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
			attr= '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>')

	"""Renders the map and saves the html file"""
	def genMap(self):
		self._map.save('index.html')

	"""Adds a run to the map. This function takes in a list of gps points and
	a color dictating what color the map should be """
	def addRun(self,gps, lineColor):
		runViz = folium.PolyLine(locations=gps, color=lineColor, opacity=0.4)
		runViz.add_to(self._map)


		

#A sample script to run to test the file
def main():
	#We only want to import json for testing
	import json

	gps =[]
	#get the path data from an example json file
	with open('gps.json') as data_file:    
		gps = json.load(data_file)

	#Create the base map centered on the most recent run
	m = RunMap(gps[0][0])

	#Create color gradient
	red = Color("red")
	colors = list(red.range_to(Color("blue"),len(gps)))
	#add each of the runs with a different color
	for i in range(len(gps)):
		m.addRun(gps[i],colors[i].hex)

	#same the html of the map so we can look at it
	m.genMap()





if __name__ == '__main__':
	main()