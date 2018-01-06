import folium
from colour import Color
import collections

"""This class represents a map of a single running area"""
class AreaMap:
	def __init__(self, mapID, numRuns, startPoint, baseMap, attr, colorGrad):

		#Set the memeber variables

		#Public
		self.mapID = mapID
		self.startPoint = startPoint

		#Private
		self._baseMap = baseMap
		self._attr = attr
		self._numRuns = numRuns
		self._colors = colorGrad
		self._runList = collections.deque()

	"""Generate the map html for this area"""
	def genMap(self):
		mapViz = folium.Map(location=self.startPoint,
				zoom_start=12,
				tiles= self._baseMap,
				attr= self._attr)

		for i in range(len(self._runList)):
			runViz = folium.PolyLine(locations=self._runList[i], color=self._colors[i].hex, opacity=0.4)
			runViz.add_to(mapViz)

		#save the map to the map file
		mapViz.save('templates/maps/map'+ str(self.mapID) +'.html')

	"""Add a run to the run map and delete the oldest one if need be"""
	def addRun(self,gps):
		#if we have to many runs then remove the oldest run from this list (which is the first one)
		if len(self._runList) == self._numRuns:
			self._runList.popleft()

		#add the run to the list
		self._runList.append(gps)

