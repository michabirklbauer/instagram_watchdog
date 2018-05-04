#!/usr/bin/env python3

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

def createConfig(users_ids, path_to_config_file):
	users_media_counts = []
	users_profile_pics = []

	for user_id in user_ids:
		users_media_counts.append(getMediaCount(user_id))
		users_profile_pics.append(getProfilePic(user_id))

	config_f = open(path_to_config_file, "w")
	string_to_write = ""
	for mc in users_media_counts:
		string_to_write = string_to_write + str(mc) + "\n"
	p = 0
	for pb in users_profile_pics:
		if p < len(users_profile_pics)-1:
			string_to_write = string_to_write + str(pb) + "\n"
		else:
			string_to_write = string_to_write + str(pb)
	config_f.write(string_to_write)
	config_f.close()

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

def instaBotSynology(path_to_config_file, user_ids, user_names, channel, api_token):
	config_f = open(path_to_config_file, "r")
	config = config_f.read().splitlines()
	config_f.close()

	users_media_counts = config[:int(len(config)/2)]
	users_profile_pics = config[int(len(config)/2):]

	rep = 1
	while rep < 60:
		rep = rep + 1
		time.sleep(60)
		for i in range(len(user_ids)):		
			new_media_count = getMediaCount(user_ids[i])
			if new_media_count > int(users_media_counts[i]):
				users_media_counts[i] = new_media_count
				new_post = getNewPost(user_names[i])
				text = "User "+str(user_names[i])+" posted something new: "+new_post[0]+" ;"
				sendMessage(text, channel, api_token)
				text = "Raw image can be found here: "+new_post[1]+" ;"
				sendMessage(text, channel, api_token)
			new_profile_pic_url = getProfilePic(user_ids[i])
			if new_profile_pic_url != users_profile_pics[i]:
				users_profile_pics[i] = new_profile_pic_url
				text = "User "+str(user_names[i])+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
				sendMessage(text, channel, api_token)
	
	config_f = open(path_to_config_file, "w")
	string_to_write = ""
	for mc in users_media_counts:
		string_to_write = string_to_write + str(mc) + "\n"
	p = 0
	for pb in users_profile_pics:
		if p < len(users_profile_pics)-1:
			string_to_write = string_to_write + str(pb) + "\n"
		else:
			string_to_write = string_to_write + str(pb)
	config_f.write(string_to_write)
	config_f.close()

if __name__ == '__main__':

	user_ids = []
	user_names = []

#	createConfig("absolute_path", user_ids)
	instaBotSynology("absolute_path",user_ids, user_names, "channel", "api_token")
