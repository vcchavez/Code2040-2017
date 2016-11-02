import requests, json
import dateutil.parser
from datetime import timedelta
from credentials import TOKEN, GITHUB, LINK #imports necessary token and links

#stage 1 of the challenge, connect to the api
def register():
	jsonRequest = {'token': TOKEN,'github': GITHUB}
	postRequest = requests.post(LINK+'/register', jsonRequest)

#stage 2, part 2 of the challenge: send the reversed string back to the api
def validate(str):
	jsonRequest = {'token': TOKEN,'string': str}
	postRequest = requests.post(LINK+'/reverse/validate', jsonRequest)

#stage 2, part 1 of the challenge: get a word from the api and reverse it
def reverse():
	jsonRequest = {'token': TOKEN}
	postRequest = requests.post(LINK+'/reverse', jsonRequest)
	if (postRequest.status_code == 200):
		validate(postRequest.text[::-1]) #[::-1] reverses a string by slicing

#stage 3, part 2: find needle in the list haystack and send the index of needle to the api
def send_needle(needle, haystack):
	for i in range(0, len(haystack)):
		if haystack[i] == needle:
			jsonRequest = {'token': TOKEN, 'needle': i}
			postRequest = requests.post(LINK+'/haystack/validate', jsonRequest)

#stage 3, part 1: get a word and list from the api
def get_haystack():
	jsonRequest = {'token': TOKEN}
	postRequest = requests.post(LINK+'/haystack', jsonRequest)
	if (postRequest.status_code == 200):
		send_needle(postRequest.json().get('needle'), 
			postRequest.json().get('haystack'))

#stage 4, part 2: find all the words in array that don't begin with prefix, add them to
	#a list and send the list to the api
def find_prefixes(prefix, array):
	list = []
	for word in array:
		if not word.startswith(prefix):
			list.append(word)
	jsonRequest = {'token': TOKEN, 'array': list}
	headers = {'content-type': 'application/json'}
	postRequest = requests.post(LINK+'/prefix/validate', json=jsonRequest, headers=headers)

#stage 4, part 1: get a word and list from the api
def prefix():
	jsonRequest = {'token': TOKEN}
	postRequest = requests.post(LINK+'/prefix', jsonRequest)
	if (postRequest.status_code == 200):
		find_prefixes(postRequest.json().get('prefix'),
			postRequest.json().get('array'))

#stage 5, part 2: add the interval time to datestamp and send it to the api in ISO format
def update_time(datestamp, interval):
	delta = timedelta(seconds=interval)
	date = dateutil.parser.parse(datestamp)
	date += delta
	headers = {'content-type': 'application/json'}
	#hacky way to append th Z for UTC but datetime specifies UTC time as +00:00
	jsonRequest = {'token': TOKEN, 'datestamp': date.isoformat()[:-6]+'Z'}
	postRequest = requests.post(LINK+'/dating/validate', json=jsonRequest, headers=headers)

#stage 5, part 1: get a date in so format and an interval time
def dating():
	jsonRequest = {'token': TOKEN}
	postRequest = requests.post(LINK+'/dating', jsonRequest)
	if (postRequest.status_code == 200):
		print postRequest.json().get('datestamp')
		update_time(postRequest.json().get('datestamp'),
			postRequest.json().get('interval'))