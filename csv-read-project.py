

'''
This is an example application for using GLAMpipe API.
Application creates a project, adds some documents to it and detects language of 'text' field
'''

import requests
import json
url = "http://localhost:3000/api/v1"

def createProject(title):
	print('Creating project')
	title = "Python: " + title
	payload = {'title': title}
	r = requests.post(url + "/projects", data=payload)
	#print(r.text)
	parsed = json.loads(r.text)
	return parsed['project']['_id']

def createCollection(project):
	data = {'params': {'title':  'my collection'}}
	print('Adding collection to project')
	r = requests.post(url + "/projects/" + project + "/nodes/collection_basic?type=collection", json=data)
	parsed = json.loads(r.text)
	return parsed['collection']


def deleteTestProjects():
	r = requests.get(url + "/projects/titles")
	parsed = json.loads(r.text)
	for p in parsed:
		if "Python" in p['title']:
			c = requests.delete(url + "/projects/" + p['_id'])
			print("Deleted " + p['title'])

def addDocument(doc, collection):
	print("Add document")
	r = requests.post(url + "/collections/" + collection + "/docs/", json=doc)

def addNode(nodetype, params, project):
	print("adding node " + nodetype)
	r = requests.post(url + "/projects/" + project + "/nodes/" + nodetype, json=params)
	parsed = json.loads(r.text)
	return parsed['id']

def runNode(node_id, settings):
	print("running node " + node_id)
	r = requests.post(url + "/nodes/" + node_id + "/run", json=settings)

def getAllDocs(collection):
	r = requests.get(url + "/collections/" + collection + "/docs")
	return json.loads(r.text)
	

# main program
project_id = createProject("csv-read")
collection_id = createCollection(project_id)

# upload local csv file (about 50 000 items)
# dataset: http://www.hri.fi/fi/dataset/helsingin-kaupunginorkesterin-konsertit
#files = {'file': open('files/Concerts_of_Helsinki_City_Orchestra.csv','rb')}
#r = requests.post(url + "/upload", files=files)
#print(r.text)
#parsed = json.loads(r.text)
#filename = parsed['filename']


file_url = 'http://www.hel.fi/hel2/tietokeskus/data/helsinki/kulttuuri/Helsingin_kaupunginorkesterin_konsertit.csv'

# add online csv read node
params = {'file_url': file_url}
data = {'params': params, 'collection': collection_id}
csv_read = addNode('source_web_csv', data, project_id);

# run csv readn node
print("Reading CSV...")
settings = {'separator': ';', 'encoding': 'latin1', 'columns': 'true'}
runNode(csv_read, settings)
print("Done!")

# get top 10 composers from facet api
r = requests.get(url + "/collections/" + collection_id + "/facet?fields=composer")
docs = json.loads(r.text)

print('************** TOP 10 Composers ****************')
for i in range(10): 
	doc = docs['facets'][0]['composer'][i]
	print(doc['_id'] + '  -> ' + str(doc['count'])) 
print('************************************************')

# uncomment this to delete all python test projects
#deleteTestProjects()

