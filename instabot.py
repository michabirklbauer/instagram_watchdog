#!/usr/bin/env python3

import urllib.request as ur
import urllib.parse as up
import datetime
import json
import time
import os

class InstaBot:

	def __init__(self, path_to_config_file, channel, api_token):
		self.path_to_config_file = path_to_config_file
		self.channel = channel
		self.api_token = api_token

	def getUserName(self, user_id):
		time.sleep(5)
		url = url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]
		return str(user_name)

	def getMediaCount(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		media_count = json.loads(user_info)["user"]["media_count"]
		return int(media_count)

	def getProfilePic(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		return str(profile_pic_url)

	def sendMessage(self, text):
		r = ur.urlopen("https://api.telegram.org/bot"+self.api_token+"/sendMessage?", up.urlencode({"chat_id": self.channel, "text": text}).encode("utf-8")).read()
		print(r)
		return

	def getNewPost(self, user_id):
		user_name = self.getUserName(user_id)
		time.sleep(5)
		url = "https://instagram.com/"+str(user_name)+"/"
		user_profile = ur.urlopen(url).read()
		post_page = "https://instagram.com/p/"+str(str(user_profile).split("shortcode")[1].split("\"")[2])
		post_pic = str(str(user_profile).split("shortcode")[1].split("display_url")[1].split("\"")[2])
		return [post_page, post_pic]

	def getStories(self, user_ids):
		self.sendMessage("Today's Stories:")
		time.sleep(5)
		for user_id in user_ids:
			user_name = self.getUserName(user_id)
			u = ur.urlopen("https://storiesig.com/?username="+str(user_name))
			time.sleep(5)
			story_link = "https://storiesig.com/stories/"+str(user_name)
			self.sendMessage(story_link)
			time.sleep(5)

	def createConfig(self, user_ids):
	
		users_media_counts = []
		users_profile_pics = []

		for user_id in user_ids:
			users_media_counts.append(self.getMediaCount(user_id))
			users_profile_pics.append(self.getProfilePic(user_id))

		config_f = open(self.path_to_config_file, "w")
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

	def writeConfig(self, users_media_counts, users_profile_pics):
	
		config_f = open(self.path_to_config_file, "w")
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

	def instaBot(self, user_ids, rtime = 3480, stime = 21):

		user_names = []
		for user_id in user_ids:
			user_names.append(self.getUserName(user_id))

		print("InstaBot initiated with usernames: ", user_names)

		if os.path.isfile(self.path_to_config_file):
			print("Found existing configuration file!")
		else:
			self.createConfig(user_ids)
			print("Created configuration file at: ", self.path_to_config_file)
	
		config_f = open(self.path_to_config_file, "r")
		config = config_f.read().splitlines()
		config_f.close()
	
		users_media_counts = config[:int(len(config)/2)]
		users_profile_pics = config[int(len(config)/2):]
	
		if rtime != 0:
			rep = 1
			while rep < rtime:
				rep = rep + 60
				time.sleep(60)
				for i in range(len(user_ids)):
					rep = rep + 5
					new_media_count = self.getMediaCount(user_ids[i])
					if new_media_count > int(users_media_counts[i]):
						users_media_counts[i] = new_media_count
						rep = rep + 5
						new_post = self.getNewPost(user_ids[i])
						text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
						self.sendMessage(text)
						text = "Raw image can be found here: "+new_post[1]+" ;"
						self.sendMessage(text)
						text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)
					rep = rep + 5
					new_profile_pic_url = self.getProfilePic(user_ids[i])
					if new_profile_pic_url != users_profile_pics[i]:
						users_profile_pics[i] = new_profile_pic_url
						text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)
	
			self.getStories(user_ids)
			print("Done! Restart?")
		else:
			try:
				while True:
					time.sleep(60)
					for i in range(len(user_ids)):
						new_media_count = self.getMediaCount(user_ids[i])
						if new_media_count > int(users_media_counts[i]):
							users_media_counts[i] = new_media_count
							new_post = self.getNewPost(user_ids[i])
							text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
							self.sendMessage(text)
							text = "Raw image can be found here: "+new_post[1]+" ;"
							self.sendMessage(text)
							text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
						new_profile_pic_url = self.getProfilePic(user_ids[i])
						if new_profile_pic_url != users_profile_pics[i]:
							users_profile_pics[i] = new_profile_pic_url
							text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
					if datetime.datetime.now().time().hour == stime and datetime.datetime.now().time().minute == 0:
						self.getStories(user_ids)
			except KeyboardInterrupt:
				try:
					self.writeConfig(users_media_counts, users_profile_pics)
				except:
					pass

				print("Exiting!")
		return

if __name__ == '__main__':

	user_ids = []

	IB = InstaBot("instabot.synconf", "", "")

	IB.instaBot(user_ids, 0, 21)
