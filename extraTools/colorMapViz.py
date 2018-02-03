from colour import Color
import matplotlib.pyplot as plt
from matplotlib import colors as mpc
from matplotlib.widgets import Slider, Button, RadioButtons

def createGrad(startColor=Color("#FFA13D"), endColor=Color("#0D1D3B")):
	#Create the color gradient
	colorGrad = list(startColor.range_to(endColor, 30))

	#Adjust the color gradient to be returned in a form that pyplot can accept
	return list(map(lambda x: x.hex, colorGrad))

def update(sliders, plotToChange, fig):
	sC = [sliders[0].val, sliders[1].val, sliders[2].val]
	eC = [sliders[3].val, sliders[4].val, sliders[5].val]

	startColor = Color(rgb = sC)
	endColor=Color(rgb =eC)

	stuff = createGrad(startColor=startColor, endColor=endColor)
	
	map(lambda x: plotToChange[x].set_color(stuff[x]),range(30))
	fig.canvas.draw_idle()


if __name__ == '__main__':
	#Create the first Bar Plot
	fig = plt.figure()
	plt.subplots_adjust(left=0.1, bottom=0.25)
	colorPlot = plt.bar(range(30), 30*[1],color = createGrad())
	plt.xlabel("Run Number")

	
	#Pick the location for the color sliders
	axRedStart = plt.axes([0.1, 0.15, 0.3, 0.03])
	axGreenStart = plt.axes([0.1, 0.1, 0.3, 0.03])
	axBlueStart = plt.axes([0.1, 0.05, 0.3, 0.03])

	axRedEnd = plt.axes([0.6, 0.15, 0.3, 0.03])
	axGreenEnd = plt.axes([0.6, 0.1, 0.3, 0.03])
	axBlueEnd = plt.axes([0.6, 0.05, 0.3, 0.03])

	#Atatch the slider objects to the sliders
	sRedStart = Slider(axRedStart, 'Red', 0, 1, valinit=1)
	sGreenStart = Slider(axGreenStart, 'Green', 0, 1, valinit=.631)
	sBlueStart = Slider(axBlueStart, 'Blue', 0, 1, valinit=.239)

	sRedEnd = Slider(axRedEnd, 'Red', 0, 1, valinit=0.05)
	sGreenEnd = Slider(axGreenEnd, 'Green', 0, 1, valinit=.114)
	sBlueEnd = Slider(axBlueEnd, 'Blue', 0, 1, valinit=.231)


	#Create a list of all the sliders
	sliders = [sRedStart, sGreenStart, sBlueStart, sRedEnd, sGreenEnd, sBlueEnd]
	

	#Provide an update function for the sliders to call and connect it to the slider
	updateFunction = lambda x: update(sliders, colorPlot, fig)
	map(lambda slider: slider.on_changed(updateFunction), sliders)

	#Display the plot
	plt.show()
	