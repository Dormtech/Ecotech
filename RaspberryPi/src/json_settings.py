import json

settings_json = json.dumps([
	{
		"type":	"title",
		"title": "Basic Settings"
	},
	{
		"type":"options",
		"title":"Units",
		"desc":"Choose either metric or imperial units",
		"section":"Basic",
		"options":['Metric', 'Imperial'],
		"key":"Units",
	},
	{
		"type": 'options',
		'title': 'Colour',
		'desc':'Choose the background colour',
		'section': 'Basic',
		'options':['Black','Blue','Red'],
		'key':"Colour",
	}
])
