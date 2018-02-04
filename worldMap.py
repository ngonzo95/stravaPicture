import folium


f = open("templates/maps/map2.html","r")
popUpString = f.read()

"""This class represents a map of a single running area"""
class WorldMap:
	def __init__(self, mapID, startPoint, baseMap, attr):

		#Set the memeber variables

		#Public
		self.mapID = mapID

		self.startPoint = startPoint

		#Private
		self._baseMap = baseMap
		self._attr = attr
		self._areaList = []

	"""Generate the map html for this area"""
	def genMap(self):
		#This deals with the case where the runList is not full
		mapViz = folium.Map(location=self.startPoint,
				zoom_start=3,
				tiles= self._baseMap,
				attr= self._attr)

		for loc, name, areaMapID in self._areaList:
			popUpHTML = '<a href=index' + str(areaMapID) + '.html>'+ name + '</a>'
			areaViz = folium.Marker(loc, popup=popUpHTML)
			areaViz.add_to(mapViz)

		#save the map to the map file
		mapViz.save('templates/maps/map'+ str(self.mapID) +'.html')

	"""Add a run to the run map and delete the oldest one if need be"""
	def addArea(self,loc, name, areaMapID):
		
		self._areaList.append((loc,name,areaMapID))

