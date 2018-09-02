#! python3
#email_creator.py - creates a hotmail address based on input username

import requests, bs4, sys, webbrowser, time, os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')

url = 'https://login.live.com/'

user = input('Username/email: ')
password = ''

print('Creating email: '+ user + '\n')

print("Connecting to Hotmail...")

#Open Firefox
browser = webdriver.Firefox(firefox_binary=binary)
browser.get(url)
time.sleep(1.5)

#Press Sign Up link
elem = browser.find_element_by_id('signup')
elem.click()
time.sleep(2.5)

sys.exit(0)

#Select "Make new email"
elem = browser.find_element_by_id('liveEasiSwitch')
elem.click()
time.sleep(1.5)

#Type input username into email field
elem = browser.find_element_by_id('MemberName')
elem.click()
elem.send_keys(user)
time.sleep(2)

#Click Password box to check if email is available
elem = browser.find_element_by_id('memberNameDomain')
print('found: '+str(type(elem)))
elem.click()
time.sleep(2)

elem = browser.find_element_by_id('suggLink')

print(type(elem))


sys.exit(0)






try:
    res = requests.get(url)
    res.raise_for_status()
except Exception as e:
    print("Error: %s" %(e))
    sys.exit(1)


soup = bs4.BeautifulSoup(res.text, "html.parser")
numPics = soup.select('span[class="active"]')
numPics = numPics[0].getText().split('[ ')
numPics = numPics[1].split(' ]')
numPics = int(numPics[0])
print('Detected '+ str(numPics) + ' images.')


#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#driver.execute_script("window.scrollTo(0, Y)")
