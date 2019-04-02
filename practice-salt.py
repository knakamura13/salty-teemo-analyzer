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

options = Options()
options.headless = True
browser = webdriver.Chrome('/Users/kjnakamura/Desktop/chromedriver', chrome_options=options)

def fetchHtmlForThePage(url, delay, block_name):
	browser.get(url)
	time.sleep(delay)

	html = ""

	try:
		# Search for an element.
		element_present = EC.presence_of_element_located((By.TAG_NAME, block_name))
		WebDriverWait(browser, 0).until(element_present)

		# Return page HTMl.
		html = browser.page_source
	except TimeoutException:
		print("Loading timed out.")

	browser.quit()

	return html


def processFetchedUrls(soup):
	rows = soup.find_all(['tr'])
	i = 0
	for row in rows:
		if (i == 0):
			i += 1
			continue
		if (i == 1):
			print('Blue Team')
		elif (i == 6):
			print('Red Team')

		percentages = row.find_all(['b'])
		print('Player {}'.format(i))
		avg = 0.0
		count = 1.0
		for percentage in percentages:
			num = float(percentage.text.split('%')[0])
			avg = (avg + num) / count
			count += 1
			print(avg)
		print('')

		i += 1


url = "https://gameinfo.saltyteemo.com"
html = fetchHtmlForThePage(url, 10, 'b')

if (html):
	soup = BeautifulSoup(html)
	processFetchedUrls(soup)
else:
	print('No soup for you.')