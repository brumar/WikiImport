import logging, json, importio, latch, csv

dataRows=[]#usefull to get the datas
dataRows2=[]#usefull to get the datas

class AnkiCard:
		front=""
		back=""
		def __init__(self, q, a):
				self.front=q.encode('utf8', 'ignore')
				self.back=a.encode('utf8', 'ignore')


def GenerateAnkiCardsFromWikipediaCategory(url,deckName,user_id,api_key):
		cards=[]
		client = importio.importio(user_id=user_id,api_key=api_key , host="https://query.import.io")
		client.connect()
		global queryLatch
		queryLatch = latch.latch(1)
		client.query({
				"connectorGuids": [
						"68b4b6ac-25ce-434d-923d-7cc9661216ff"#7fc7daa2-25a4-4649-b48c-be1d7fd8756e
				],
				"input": {
						"webpage/url": url
				}
		}, callback)
		print "Queries dispatched, now waiting for results"
		queryLatch.await()
		print json.dumps(dataRows, indent = 4)
		#print(dataRows[0]["title"])
		queryLatch = latch.latch(len(dataRows))
		for data in dataRows :
			if('url' in data.keys()):
								client.query({
										"connectorGuids": [
						"7fc7daa2-25a4-4649-b48c-be1d7fd8756e"
										],
										"input": {
														"webpage/url": data['url']
										}
						}, callback2)

		queryLatch.await()
		print json.dumps(dataRows2, indent = 4)
		for d in dataRows2:
			if(all(x in d.keys() for x in ["title","first_par"])):
				cards.append(AnkiCard(d["title"],d["first_par"]))
		client.disconnect()
		reinitGlobalVariables()
		return cards

def reinitGlobalVariables():
	global dataRows
	global dataRows2
	dataRows=[]
	dataRows2=[]

def callback2(query, message):
		global dataRows2

		# Disconnect messages happen if we disconnect the client library while a query is in progress
		if message["type"] == "DISCONNECT":
				print "Query in progress when library disconnected"
				print json.dumps(message["data"], indent = 4)

		# Check the message we receive actually has some data in it
		if message["type"] == "MESSAGE":
				if "errorType" in message["data"]:
						# In this case, we received a message, but it was an error from the external service
						print "Got an error!"
						print json.dumps(message["data"], indent = 4)
				else:
						# We got a message and it was not an error, so we can process the data
						print "Got data!"
						print json.dumps(message["data"], indent = 4)
						# Save the data we got in our dataRows variable for later
						dataRows2.extend(message["data"]["results"])

		# When the query is finished, countdown the latch so the program can continue when everything is done
		if query.finished(): queryLatch.countdown()

def callback(query, message):
	global dataRows

	# Disconnect messages happen if we disconnect the client library while a query is in progress
	if message["type"] == "DISCONNECT":
		print "Query in progress when library disconnected"
		print json.dumps(message["data"], indent = 4)

	# Check the message we receive actually has some data in it
	if message["type"] == "MESSAGE":
		if "errorType" in message["data"]:
			# In this case, we received a message, but it was an error from the external service
			print "Got an error!"
			print json.dumps(message["data"], indent = 4)
		else:
			# We got a message and it was not an error, so we can process the data
			print "Got data!"
			print json.dumps(message["data"], indent = 4)
			# Save the data we got in our dataRows variable for later
			dataRows.extend(message["data"]["results"])

	# When the query is finished, countdown the latch so the program can continue when everything is done
	if query.finished(): queryLatch.countdown()


def printCardsAsCsv(cards,filename):
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for card in cards:
				writer.writerow([card.front]+[card.back.replace(";",",")])

# Issue queries to your data sources and with your inputs
# You can modify the inputs and connectorGuids so as to query your own sources
# Query for tile First paragraphe wikipedia (crawler)
if __name__ == "__main__":
	dataRows=[]
	dataRows2=[]
	user_id="93e6a27f-a52e-4ecc-8c70-79b1df692285"
	api_key=""#complete this line
	url="http://en.wikipedia.org/wiki/Category:Statistical_paradoxes"
	deckName="StatParadoxes"
	cards=GenerateAnkiCardsFromWikipediaCategory(url,deckName,user_id,api_key)
	printCardsAsCsv(cards,deckName+".csv")




