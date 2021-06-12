# Purpose: Create list of volunteering opportunities based on text filter
# Author: Heath Gilham
# Logic: Download HTML from websites. Find roles and link based on class / href tag. Export roles to file for those which haven't already been checked.
# Instructions: 1. Change words to search on line 27 
#               2. Run in python intepreter
#				3. Check through whole list and copy link into chrome if interested

# Import Libraries
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import requests
import time
import sys    

# Define Functions
def Log(Text):
    
    Timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S%p")
    Text = Timestamp + " " + Text 
    print(Text)
    with open(LogFile, "a") as TextFile:
        TextFile.write(Text + "\n")

# Customise volunteer roles exported
RoleIncludesText = ['grant','fundrais']

# Define Variables
os.chdir(os.path.dirname(__file__))
StartTime = datetime.now() 
Datetime = datetime.now().strftime("%d%m%Y_%I%M%p")
Date = datetime.now().strftime("%d-%m-%Y")
DateForFile = datetime.now().strftime("%-d/%-m/%Y %I:%M:%S%p")
LogFolder = "Log/"
LogFile = LogFolder + "/" + Date + ".log"
IsDebuggingMode = False
OldFileDirName = "Old_files"
CSVCheckedFile = "custom_volunteer_options.csv"
CurrentCheckedLinks = []
if not os.path.exists(LogFolder):  os.makedirs(LogFolder)
if not os.path.exists(LogFile):  open(LogFile,"w")
if not os.path.exists(CSVCheckedFile): csv.writer(open(CSVCheckedFile,'w'), quoting=csv.QUOTE_ALL).writerow(["Date Checked","Role","Link"])
OpenCurrentFile = open(CSVCheckedFile,'a')
CurrentCSVWriter = csv.writer(OpenCurrentFile, quoting=csv.QUOTE_NONE)

PreviousCheckedLinks = [line[2] for line in csv.reader(open(CSVCheckedFile, "r"))]
            
Log("Running " + os.path.basename(sys.argv[0]))


Log("Collecting Volunteer.com.au in person data")

rolesperpage = 15               
rolecount = 15 
pagenum = 0              
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://www.volunteer.com.au/volunteering/in-melbourne-cbd-inner-suburbs-melbourne-vic?daytime=1%2C3&page=" + str(pagenum)).content
    ATags = BeautifulSoup(srcdata, features = "html.parser").find_all("a")
    
    rolecount = 0
    for tag in ATags:
        
        try:
            TagClass = tag.attrs['class']
        except:
            TagClass = ""
        
        if "sc-1lrhu3b-3" in TagClass:
            rolecount += 1
            href = tag.attrs['href']
            URL = "https://www.volunteer.com.au" + href

            if URL not in PreviousCheckedLinks and URL not in CurrentCheckedLinks:
                if any(x.lower() in tag.text.replace(",",";").replace('"',";").lower() for x in RoleIncludesText):
                    CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";").replace('"',";"), URL])
                    CurrentCheckedLinks += [URL]
        
Log("New Volunteer.com.au in person roles added to csv")


Log("Collecting Volunteer.com.au online data")

rolesperpage = 15
rolecount = 15
pagenum = 0
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://www.volunteer.com.au/volunteering/in-online-or-remote?daytime=1%2C3&page=2" + str(pagenum)).content
    ATags = BeautifulSoup(srcdata, features = "html.parser").find_all("a")
    
    rolecount = 0
    for tag in ATags:
        
        try:
            TagClass = tag.attrs['class']
        except:
            TagClass = ""
        
        if "sc-1lrhu3b-3" in TagClass:
            rolecount += 1
            href = tag.attrs['href']
            URL = "https://www.volunteer.com.au" + href
      
            if URL not in PreviousCheckedLinks and URL not in CurrentCheckedLinks:
                if any(x.lower() in tag.text.replace(",",";").replace('"',";").lower() for x in RoleIncludesText):
                    CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";").replace('"',";"), URL])
                    CurrentCheckedLinks += [URL]
        
Log("New Volunteer.com.au online roles added to csv")


Log("Collecting GoVolunteer data")

rolesperpage = 20               
rolecount = 20 
pagenum = 0               
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://govolunteer.com.au/volunteering/in-melbourne-vic-3000?page=" + str(pagenum) + r"&radius=5&youravailability=3%2c5").content
    a_tags = BeautifulSoup(srcdata, features = "html.parser").find_all("a")
    
    rolecount = 0
    for tag in a_tags:
        
        try:
            href = tag.attrs['href']
        except:
            href = ""

        if "volunteering/opportunity/" in href:
            rolecount += 1
            URL = "https://govolunteer.com.au" + href[:-1]

            if URL not in PreviousCheckedLinks and URL not in CurrentCheckedLinks:
                if any(x.lower() in tag.text.replace(",",";").replace('"',";").lower() for x in RoleIncludesText):
                    CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";").replace('"',";"), URL])
                    CurrentCheckedLinks += [URL]
            
Log("New GoVolunteer roles added to csv")

OpenCurrentFile.close()
EndTime = datetime.now() 
Log("Time Taken: " + str(EndTime - StartTime))
