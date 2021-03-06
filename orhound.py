#!/usr/bin/env python

# Open Redirect Hound
#
# ORHOund is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Knock is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Knock. If not, see <http://www.gnu.org/licenses/>.

# Standard Python libraries
import sys
import requests, re
import random
import time
from bs4 import BeautifulSoup

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def banner():
	print(colors.WARNING  + """
 ___  ____  _   _                       _ 
 / _ \|  _ \| | | | ___  _   _ _ __   __| |
| | | | |_) | |_| |/ _ \| | | | '_ \ / _` |
| |_| |  _ <|  _  | (_) | |_| | | | | (_| |
 \___/|_| \_\_| |_|\___/ \__,_|_| |_|\__,_|
""" + colors.ENDC)
	print(colors.OKGREEN + "ORHound v.1.0 - Open Source Project\n" + "Author: Robotshell\n" + "Github: https://github.com/robotshell\n" + colors.ENDC)

#CORE FUNCTION
def dork(domain,enable_save):
#https://www.google.com/search?q=inurl%3A%3D%253Dhttp+site%3Atest.com
	print (colors.OKCYAN + "Starting Google Dork scraping to find Open Redirects to " + colors.FAIL + domain + colors.ENDC)

	with open("user_agent.txt") as ua:
                USER_AGENT = ua.readlines()

	query = 'inurl%3A%3D%253dhttp+site%3A'+domain
	URL = "https://google.com/search?q="+query
	headers = {"user-agent": random.choice(USER_AGENT).strip()} 
	res = requests.get(URL, headers=headers)
	#print(res.content)

	if res.status_code == 200:
		soup = BeautifulSoup(res.content, "html.parser")
		links = []
		titles = []

		for g in soup.find_all('div', class_='r'):
			anchors = g.find_all('a')
			if anchors:
				link = anchors[0]['href']
				title = g.find('h3').text
				links.append(link)
				titles.append(title)
				print(colors.WARNING + link + colors.ENDC)
	else:
		print(colors.FAIL + "Something goes wrong" + colors.ENDC)
     

#MAIN FUNCTION
def main():
	banner()
	enable_save=0 
	
	if len(sys.argv) == 1:
		print (colors.FAIL + "ERROR: No domain or parameters found" + colors.ENDC)
	else:
		arg=sys.argv[1]
		if arg == "-h" or arg == "--help" :
			print (colors.BOLD + "HELP SECTION:" + colors.ENDC)
			print ("Usage:" + colors.OKCYAN + "\torhound.py domain.com" + colors.ENDC)
			print ("-h,--help" + colors.OKCYAN + "\tThis help" + colors.ENDC)
			print ("-v,--version" + colors.OKCYAN + "\tShow version" + colors.ENDC)
			print ("-s,--save" + colors.OKCYAN + "\tEnable save output in .txt file" + colors.ENDC)
		elif arg == "-v" or arg == "--version":
			print ("ORHound v.1.0")
		elif arg == "-s" or arg == "--save":
			enable_save=1
			dork(arg,enable_save) 
		else:
			dork(arg,enable_save)
	
main()