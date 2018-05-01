#!/usr/bin/env python3

# A simple python watchdog that can watch public instagram profiles for new posts and sends notifications to a telegram channel
# uses the official Bot API by Telegram and the official instagram API
# see bottom for usage

import urllib.request as ur
import urllib.parse as up
import time

def getMediaCount(user_id):
	url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
	user_info = ur.urlopen(url).read()
	media_count = int(str(user_info).split("media_count")[1].split(":")[1].split(",")[0].lstrip().rstrip())
	return media_count

def getProfilePic(user_id):
	url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
	user_info = ur.urlopen(url).read()
	profile_pic_url = str(str(user_info).split("hd_profile_pic_url_info")[1].split("url")[1].split("\"")[2].lstrip().rstrip())
	return profile_pic_url

def sendMessage(text, channel, api_token):
	r = ur.urlopen("https://api.telegram.org/bot"+api_token+"/sendMessage?", up.urlencode({"chat_id": channel, "text": text}).encode("utf-8")).read()
	print(r)
	return

def getNewPost(user_name):
	url = "https://instagram.com/"+str(user_name)+"/"
	user_profile = ur.urlopen(url).read()
	post_page = "https://instagram.com/p/"+str(str(user_profile).split("shortcode")[1].split("\"")[2])
	post_pic = str(str(user_profile).split("shortcode")[1].split("display_url")[1].split("\"")[2])
	return [post_page, post_pic]

def instaBot(user_id, user_name, channel, api_token):
	media_count = getMediaCount(user_id)
	profile_pic_url = getProfilePic(user_id)
	text = "Running: instabot initiated for user "+str(user_name)+"; current media count: "+str(media_count)+"; current profile pic: "+str(profile_pic_url)+" ;"
	sendMessage(text, channel, api_token)
	try:	
		while True:
			time.sleep(60)		
			new_media_count = getMediaCount(user_id)
			if new_media_count > media_count:
				media_count = new_media_count
				new_post = getNewPost(user_name)
				text = "User "+str(user_name)+" posted something new: "+new_post[0]+" ;"
				sendMessage(text, channel, api_token)
				text = "Raw image can be found here: "+new_post[1]+" ;"
				sendMessage(text, channel, api_token)
			new_profile_pic_url = getProfilePic(user_id)
			if new_profile_pic_url != profile_pic_url:
				profile_pic_url = new_profile_pic_url
				text = "User "+str(user_name)+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
				sendMessage(text, channel, api_token)
	except KeyboardInterrupt:
		print("exiting")
		return
	return

if __name__ == '__main__':

	# user id e.g. 2538307007 (find out: https://inteltechniques.com/menu.html)
	user_id =
	# user name e.g. "micha_birklbauer"
	user_name =
	# a valid telegram channel that you have access to in form "@channel_name"
	channel =
	# a valid api token (as string) for a bot that has access to above channel
	api_token =
	instaBot(user_id, user_name, channel, api_token)
