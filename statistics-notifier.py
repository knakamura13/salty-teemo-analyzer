import sys
import time
import smtplib
import requests
import itertools
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from subprocess import Popen, PIPE
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




####################
# Global Constants #
####################


GAME_INFO_URL = "https://gameinfo.saltyteemo.com"

SPINNER = itertools.cycle(['|', '/', '-', '\\'])

SCRIPT = '''
on run {targetBuddyPhone, targetMessage}
	tell application "Messages"
		set targetService to 1st service whose service type = iMessage
		set targetBuddy to buddy targetBuddyPhone of targetService
		send targetMessage to targetBuddy
	end tell
end run'''




#####################
# Global Properties #
#####################


options = Options()
options.headless = True
browser = webdriver.Chrome(chrome_options=options)

prev_url = ""

curr_url = ""

first_iteration = True




#############
# Functions #
#############


def fetchHtml(url, delay):
	''' Fetch HTML Function
	
	Uses Selenium to grab the HTML contents of a web page,
	then passes the HTML, as BeautifulSoup, to `parseHtml()`.

	:param url: 	The url of the web page to grab HTML from.
	:param delay: 	The amount of seconds to wait for the page contents to finish loading.
	'''

	browser.get(url)
	time.sleep(delay)

	html = ""

	try:
		# Search for an element.
		element_present = EC.presence_of_element_located((By.TAG_NAME, 'b'))
		WebDriverWait(browser, 0).until(element_present)

		# Return page HTMl.
		html = browser.page_source
	except TimeoutException:
		print("Loading timed out.")

	browser.quit()

	if (html):
		soup = BeautifulSoup(html, 'html.parser')
		parseHtml(soup)
	else:
		print('No game info found.')

def parseHtml(soup):
	''' Parse HTML Function

	Uses BeautifulSoup to make an array of all `tr` elements on the page,
	then calculates the average win-rate of both the Blue and Red teams.

	:param soup: 	The BeautifulSoup object passed in from a successful HTML retrieval in `fetchHtml()`.
	'''

	rows = soup.find_all(['tr'])

	blue_total = 0.0
	red_total = 0.0

	blue_count = 0.0
	red_count = 0.0

	for i, row in enumerate(rows):
		if (i == 0):
			continue

		percentages = row.find_all(['b'])

		# Calculate player total.
		player_total = 0.0
		player_count = 0.0
		for percentage in percentages:
			num = float(percentage.text.split('%')[0])
			if (num):
				player_total += num
				player_count += 1.0

		# Calculate player average.
		player_average = player_total / player_count

		# Update team totals.
		if (player_average):
			if (i <= 5):
				blue_total += player_average
				blue_count += 1.0
			else:
				red_total += player_average
				red_count += 1.0

	# Calculate team averages.
	blue_average = round(blue_total / blue_count, 2)
	red_average = round(red_total / red_count, 2)

	print("Blue Average: {}%".format(blue_average))
	print("Red Average: {}%".format(red_average))




########
# Main #
########


fetchHtml(GAME_INFO_URL, 10)



