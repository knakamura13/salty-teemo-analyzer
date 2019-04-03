import sys
import time
import smtplib
import requests
import itertools
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from subprocess import Popen, PIPE
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


#############
# Constants #
#############

SPINNER = itertools.cycle(['|', '/', '-', '\\'])

SCRIPT = '''
on run {targetBuddyPhone, targetMessage}
tell application "Messages"
set targetService to 1st service whose service type = iMessage
set targetBuddy to buddy targetBuddyPhone of targetService
send targetMessage to targetBuddy
end tell
end run'''

GAME_INFO_URL = "https://gameinfo.saltyteemo.com"


##############
# Properties #
##############

options = Options()
options.headless = True
driver = webdriver.Chrome('/Users/kjnakamura/Desktop/chromedriver', chrome_options=options)

prev_url = ""

curr_url = ""

first_iteration = True


#############
# Functions #
#############

while(True):
    driver.get(GAME_INFO_URL)

    TIME = datetime.now().strftime("%I:%M %p")
    ARGS = ['6262099242', '{} - A new game has started!'.format(TIME)]

    # Create a new subprocess to execute an osascript.
    p = Popen(
        ['osascript', '-'] + ARGS, 
        stdin=PIPE, 
        stdout=PIPE, 
        stderr=PIPE, 
        encoding='utf8',
        universal_newlines=True
    )

    # Keep waiting for driver URL to redirect from original URL.
    while(driver.current_url == GAME_INFO_URL):
        time.sleep(0.1)

    # Check if the URL has changed.
    if (curr_url != prev_url):
        if (first_iteration):
            first_iteration = False
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            print(soup)
        else:
            # Parse data from game info.
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            print(soup)

            if str(soup).find("Summoner name") != -1:
                name_box = soup.find('h1', attrs={'class': 'name'})
                print('Soup contains summoner name.')
            else:
                print('No soup for you.')

            # Send a text me.
            p.stdin.write(SCRIPT)
    else:
        # Display a spinner wheel.
        sys.stdout.write(next(SPINNER))
        sys.stdout.flush()
        sys.stdout.write('\b')

    # Close the subprocess.
    p.stdin.close()
    p.wait()

    # Prepare variables for next iteration.
    prev_url = curr_url
    curr_url = driver.current_url

    # Wait 15 seconds before checking the URL again.
    time.sleep(15)
