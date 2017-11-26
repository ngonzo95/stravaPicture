#Test file used for rendering out template html
if __name__ == '__main__':
	import jinja2
	templateLoader = jinja2.FileSystemLoader( searchpath="./templates")
	templateEnv = jinja2.Environment(loader=templateLoader)
	TEMPLATE_FILE = "template.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	outputText = template.render({'maps':[{'href':'index.html', 'caption': 'hi'}, {'href':'#', 'caption': 'bye', 'current': True}]}) # this is where to put args to the template renderer

	with open("views/my_new_file.html", "wb") as fh:
		fh.write(outputText)