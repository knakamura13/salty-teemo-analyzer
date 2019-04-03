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
	rows = soup.find_all(['tr'])

	# TODO: Account for 0% win rate.
	blue_total = 0.0
	red_total = 0.0
	i = 0
	for row in rows:
		if (i == 0):
			i += 1
			continue

		percentages = row.find_all(['b'])

		avg = 0.0
		count = 1.0
		for percentage in percentages:
			num = float(percentage.text.split('%')[0])
			avg = (avg + num) / count
			count += 1

		if (i <= 5):
			blue_total += avg
		else:
			red_total += avg

		i += 1

	print("Blue:", blue_total / 5.0, "%")
	print("Red:", red_total / 5.0, "%")




########
# Main #
########


fetchHtml(GAME_INFO_URL, 10)



