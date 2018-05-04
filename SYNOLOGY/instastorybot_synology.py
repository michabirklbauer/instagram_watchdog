#!/usr/bin/env python3

import urllib.request as ur
import urllib.parse as up
import time

def sendMessage(text, channel, api_token):
	r = ur.urlopen("https://api.telegram.org/bot"+api_token+"/sendMessage?", up.urlencode({"chat_id": channel, "text": text}).encode("utf-8")).read()
	print(r)
	return

def getStories(user_names, channel, api_token):
	sendMessage("Today's Stories:", channel, api_token)
	time.sleep(5)
	for user_name in user_names:
		u = ur.urlopen("https://storiesig.com/?username="+str(user_name))
		time.sleep(5)
		story_link = "https://storiesig.com/stories/"+str(user_name)
		sendMessage(story_link, channel, api_token)
		time.sleep(5)

if __name__ == '__main__':

	user_names = []

	getStories(user_names, "channel", "api_token")
