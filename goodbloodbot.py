import sys
import pdb
from enum import Enum
import tweepy
import random
from collections import defaultdict
from secrets import *
from bb_templates import *
from ds1_templates import *
from ds2_templates import *
from ds3_templates import *
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
import datetime
tweets = []

#region Email Methods
def email_login():
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		return server
	except:  
		print('Something went wrong...')

def send_email():
	sent_from = gmail_user  
	to = ['jameslkidd@gmail.com']  
	subject = '@goodbloodbot Tweet Summary for {0}'.format(datetime.datetime.now().strftime('%d/%m/%Y'))
	body = "Subject: {0}\n\n".format(subject)
	for tweet, date in tweets:
		body += "Tweet at {0}: {1}\n\n".format(date, tweet)

	server = email_login()
	server.sendmail(sent_from, to, body)
	server.close()
#endregion

#create an OAuthHandler instance
#takes argument of account_name for multiple bots
def get_auth(account_name='goodbloodbot'):
	if account_name == 'goodbloodbot' or account_name != 'horsebothole': # default to goodbloodbot
		auth = tweepy.OAuthHandler(blood_consumer_key, blood_consumer_secret)
		auth.set_access_token(blood_access_token, blood_access_secret)
		return auth
	elif account_name == 'horsebothole':
		auth = tweepy.OAuthHandler(horse_consumer_key, horse_consumer_secret)
		auth.set_access_token(horse_access_token, horse_access_secret)
		return auth

#create the api instance
def get_api(account_name='goodbloodbot'):
	auth = get_auth(account_name)
	api = tweepy.API(auth) # create an API object
	return api

# get last tweet sent
def get_last_tweet(account_name):
	api = get_api(account_name)
	try:
		tweet = api.user_timeline(id = api.me().id, count = 1)[0]
		return tweet
	except IndexError:
		return True

# pass in "template" or "conjunction" to return templates or conjunctions
# game param decides which DS game to build for
def build_notes(account_name='goodbloodbot', templates_only=None, game=None):
	# build dictionary from lists
	notes = defaultdict(list)

	if account_name == 'goodbloodbot':
		# builds templates/conjuction only given param of "template"/"conjunction"
		if templates_only is not None:
			if "template" in templates_only:
				for template in bb_templates:
					notes["bb_templates"].append(template)
			elif "conjunction" in templates_only:
				for conjunction in bb_conjunctions: # what's your function?
					notes["bb_conjunctions"].append(conjunction)

		else:
			for creature in bb_creatures:
				notes["bb_words"].append(creature)

			for human in bb_humans:
				notes["bb_words"].append(human)

			for tactic in bb_tactics_a:
				notes["bb_words"].append(tactic)

			for tactic in bb_tactics_b:
				notes["bb_words"].append(tactic)

			for place_thing in bb_places_things:
				notes["bb_words"].append(place_thing)

			for concept in bb_concepts:
				notes["bb_words"].append(concept)

	if account_name == 'horsebothole':
		if game == 'ds1' or game == None:
			if templates_only is not None:
				if "template" in templates_only:
					for template in ds1_templates:
						notes["ds1_templates"].append(template)
			else:
				for character in ds1_characters:
					notes["ds1_words"].append(character)
				for obj in ds1_objects:
					notes["ds1_words"].append(obj)
				for technique in ds1_techniques:
					notes["ds1_words"].append(technique)
				for action in ds1_actions:
					notes["ds1_words"].append(action)
				for location in ds1_geography:
					notes["ds1_words"].append(location)
				for direction in ds1_orientation:
					notes["ds1_words"].append(direction)
				for body_part in ds1_body_parts:
					notes["ds1_words"].append(body_part)
				for attribute in ds1_attributes:
					notes["ds1_words"].append(attribute)
				for concept in ds1_concepts:
					notes["ds1_words"].append(concept)

		if game == 'ds2':
			if templates_only is not None:
				if "template" in templates_only:
					for template in ds2_templates:
						notes["ds2_templates"].append(template)
			else:
				for creature in ds2_creatures:
					notes["ds2_words"].append(creature)
				for obj in ds2_objects:
					notes["ds2_words"].append(obj)
				for technique in ds2_techniques:
					notes["ds2_words"].append(technique)
				for action in ds2_actions:
					notes["ds2_words"].append(action)
				for location in ds2_geography:
					notes["ds2_words"].append(location)
				for direction in ds2_orientation:
					notes["ds2_words"].append(direction)
				for body_part in ds2_body_parts:
					notes["ds2_words"].append(body_part)
				for attribute in ds2_attributes:
					notes["ds2_words"].append(attribute)
				for concept in ds2_concepts:
					notes["ds2_words"].append(concept)

		if game == 'ds3':
			if templates_only is not None:
				if "template" in templates_only:
					for template in ds3_templates:
						notes["ds3_templates"].append(template)

				elif "conjunction" in templates_only:
					for conjunction in ds3_conjunctions: # what's your function?
						notes["ds3_conjunctions"].append(conjunction)

			else:
				for creature in ds3_creatures:
					notes["ds3_words"].append(creature)
				for obj in ds3_objects:
					notes["ds3_words"].append(obj)
				for technique in ds3_techniques:
					notes["ds3_words"].append(technique)
				for action in ds3_actions:
					notes["ds3_words"].append(action)
				for location in ds3_geography:
					notes["ds3_words"].append(location)
				for direction in ds3_orientation:
					notes["ds3_words"].append(direction)
				for body_part in ds3_body_parts:
					notes["ds3_words"].append(body_part)
				for attribute in ds3_attributes:
					notes["ds3_words"].append(attribute)
				for concept in ds3_concepts:
					notes["ds3_words"].append(concept)

	return notes

# select type of note to generate
# todo: account for other games here?
def get_note_type(account_name='goodbloodbot', game=None):
	note_types = defaultdict(list)
	# Bloodborne templates
	if account_name == 'goodbloodbot':
		# single-line note, template with wildcard
		for component in ["template", "word"]:
			note_types["single"].append(component)
		# double-line note, template with wildcard, conjunction, template with wildcard
		for component in ["template", "word", "conjunction", "template", "word"]:
			note_types["double"].append(component)
		# return note type at random
		return note_types[list(note_types)[random.randint(0, 1)]]

	if account_name == 'horsebothole':
		if game == 'ds1' or game == 'ds2':
			for component in ["template", "word"]:
				note_types["single"].append(component)
			return note_types["single"]
		if game == 'ds3':
			# single-line note, template with wildcard
			for component in ["template", "word"]:
				note_types["single"].append(component)
			# double-line note, template with wildcard, conjunction, template with wildcard
			for component in ["template", "word", "conjunction", "template", "word"]:
				note_types["double"].append(component)
			# return note type at random
			return note_types[list(note_types)[random.randint(0, 1)]]
	
# get random value from provided or random dataset
def get_random_word(account_name='goodbloodbot', templates_only=None, game=None):
	# if no dataset provided, set one by default and use local notes variable
	notes = build_notes(account_name, templates_only, game) # if no template passed in, returns filler words
	# get random value from first key (get length by iterating thru keys and using key to get vals)
	if templates_only is None:
		dataset = "{0}_words".format(game)
	else:
		dataset = templates_only

	try:
		index = random.randint(0, len(notes[dataset]) - 1)
		return notes[dataset][index]
	except Exception as e:
		print(e)

# get random game to generate note from
def get_random_game():
	games = ['ds1', 'ds2', 'ds3']
	return games[random.randint(0, len(games) - 1)]

# builds note to tweet
def build_note(account_name='goodbloodbot', game=None):
	# get each value needed to fill
	note_type = get_note_type(account_name, game)
	note = ""

	if game == 'bb' or game == None:
		# build based on each component
		for component in note_type:
			if component == "template":
				note += get_random_word(account_name, "bb_templates")
			elif component == "word":
				if note.find('{0}') > 0: #if wildcard found anywhere but at the start of a template
					note = note.format(get_random_word(account_name, None, 'bb').lower()) # lowercase it
				else:
					note = note.format(get_random_word(account_name, None, 'bb')) #keep capitalization otherwise
			elif component == "conjunction":
				note += get_random_word(account_name, "bb_conjunctions")

	if game == 'ds1' or game == 'ds2':
		for component in note_type:
			if component == "template":
				note += get_random_word(account_name, "{0}_templates".format(game), game)
			elif component == "word":
				if note.find('{0}') > 0: #if wildcard found anywhere but at the start of a template
					note = note.format(get_random_word(account_name, None, game).lower()) # lowercase it
				else:
					note = note.format(get_random_word(account_name, None, game)) #keep capitalization otherwise
		if game == 'ds2':
			titleized_game = "(Dark Souls 2)"
		else: 
			titleized_game = "(Dark Souls)"
		note = "{0}\n\n{1}".format(note, titleized_game)

	if game == 'ds3':
		for component in note_type:
			if component == "template":
				if note == "":
					note += get_random_word(account_name, "ds3_templates", game)
				else:
					note += get_random_word(account_name, "ds3_templates", game).lower() # lowercase templates that come after conjunctions
			elif component == "word":
				if note.find('{0}') > 0: #if wildcard found anywhere but at the start of a template
					note = note.format(get_random_word(account_name, None, 'ds3').lower()) # lowercase it
				else:
					note = note.format(get_random_word(account_name, None, 'ds3')) #keep capitalization otherwise
			elif component == "conjunction":
				note += get_random_word(account_name, "ds3_conjunctions", game)
		note = "{0}\n\n(Dark Souls 3)".format(note)

	return note

# send provided string as tweet
def send_tweet(tweet, account_name='goodbloodbot'):
	api = get_api(account_name)
	# check to see if tweet is duplicate
	if tweet != get_last_tweet(account_name):
		api.update_status(tweet)
		# append tweet with timestamp to tweets variable		
		#tweets.append((tweet, datetime.datetime.now().strftime('%d/%m/%Y')))
		# send email at 12 tweets
		#if len(tweets) >= 12:
			#send_email()
			#tweets.clear()
	# generate a new one if it is
	else:
		print("Duplicated previous tweet. Generating new note.")
		tweet = build_note(account_name, get_random_game())
		api.update_status(tweet)
		# append tweet with timestamp to tweets variable
		#tweets.append((tweet, datetime.datetime.now().strftime('%d/%m/%Y')))
		# send email at 12 tweets
		#if len(tweets) >= 12:
			#send_email()
			#tweets.clear()

# sends generate note tweet
def tweet_job(account_name):
	if account_name == 'horsebothole':
		tweet = build_note(account_name, get_random_game())
		send_tweet(tweet, account_name)
		print("Sent tweet on @{0}: {1}".format(account_name, tweet))
	else:
		tweet = build_note(account_name)
		send_tweet(tweet, account_name)
		print("Sent tweet on @{0}: {1}".format(account_name, tweet))

# scheduler to send tweet every n minutes
def start_scheduler(interval, account_name):
	scheduler = BlockingScheduler()
	scheduler.add_job(lambda: tweet_job(account_name), 'interval', minutes=interval)
	scheduler.start()

class stream_listener(tweepy.StreamListener):
	def on_event(self, status):
		print(status)
		print(status.event)
		if status.event == 'favorite':
			pass  # handle event here

# todo: account_name here?
def get_stream_listener(account_name):
	myStream = tweepy.Stream(auth = get_auth(account_name), listener=stream_listener())
	myStream.userstream()

def BotListener():
	# get account name passed in on arg
	if len(sys.argv) >= 2: # if there are arguments
		account_name = sys.argv[1] # first argument is account_name; 'goodbloodbot' or 'horsebothole'
		# todo: other arguments here, like tweet time? email enabled?
	elif len(sys.argv) <= 1: # if no arguments
		account_name = 'goodbloodbot' # default to goodbloodbot

	api = get_api(account_name)
	auth = get_auth(account_name)
	# get_stream_listener()

	while True:
		# if account_name == 'horsebothole':
			# tweet = build_note(account_name, get_random_game())
		# else:
			# tweet = build_note(account_name)

		print("Sending start-up tweet...")
		tweet_job(account_name)
		start_scheduler(60, account_name)
		# send_tweet(tweet, account_name)
		# command = input("Command: ")
		# if "tweet" in command:
			# tweet_job(account_name)
			# print(build_note(account_name, get_random_game() if account_name == 'horsebothole' else None))
		# elif "run" in command:
			# interval = command.split(" ")[1]
			# print("Sending tweet every {0} minutes.\n".format(interval))
			# print("Sending start-up tweet...")
			# send_tweet(build_note(account_name, get_random_game()), account_name)
			# start_scheduler(int(interval), account_name)
		#elif "email" in command:
		#	send_email()
		# elif "quit" in command or command == "q":
			# break
		# else:
			# print("Invalid command.")

BotListener()
