from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import requests
import sys
import time

# Define Functions
def Log(Text):
    
    Timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S%p")
    Text = Timestamp + " " + Text 
    print(Text)
    with open(LogFile, "a") as TextFile:
        TextFile.write("Now the file has more content!")
        TextFile.close()

# Define Variables
os.chdir(os.path.dirname(__file__))
StartTime = datetime.now() 
Datetime = datetime.now().strftime("%d%m%Y_%I%M%p")
Date = datetime.now().strftime("%d-%m-%Y")
DateForFile = datetime.now().strftime("%d/%m/%Y")
LogFolder = "Log/"
LogFile = LogFolder + "/" + Date + ".log"
if not os.path.exists(LogFolder):  os.makedirs(LogFolder)
if not os.path.exists(LogFile):  open(LogFile,"w")

CSVExportFile = "club_info.csv"
CSVClubNumberFile = "club_numbers.csv"
csv.writer(open(CSVExportFile,'w'), quoting=csv.QUOTE_ALL).writerow(["CharterDate", "Website", "Facebook", "MeetingTimes", "Location", "Restrictions"])
OpenCurrentFile = open(CSVExportFile,'a')
CurrentCSVWriter = csv.writer(OpenCurrentFile, quoting=csv.QUOTE_ALL)

Log("Running " + os.path.basename(sys.argv[0]))

Log("Collecting club data")

OpenClubNumberFile = open(CSVClubNumberFile,'r')
for ClubNumber in csv.reader(OpenClubNumberFile):
    ClubNumber = ClubNumber[0]
    Log("Finding data for club " + ClubNumber)
    
    srcdata = requests.get("https://www.toastmasters.org/Find-a-Club/" + format(int(ClubNumber[0]), '08d')).content
    content = BeautifulSoup(srcdata, features = "html.parser")

    Info = content.find("div", class_="info")
    
    try:
        CharterDate = Info.findChildren("dd")[1].text
    except:
        CharterDate = ""

    try:
        Links = Info.findChildren("a")
    except:
        Links = ""

    try:
        Website = Links[0]['href']
    except:
        Website = ""

    try:
        Facebook = Links[1]['href']
    except:
        Facebook = ""

    try:
        MeetingTimes = content.find_all("div", class_="contact-info-meeting-times")[0].text.strip().replace("Meeting Times: ","")
    except:
        MeetingTimes = ""
        
    try:    
        Location = content.find_all("div", class_="contact-info-body")[0].text.replace("Location:","").strip()
    except:
        Location = ""

    try:    
        Restrictions = content.find_all("div", class_="contact-info-restriction")[0].text.replace("Membership Restriction:","").strip()
    except:
        Restrictions = ""

    CurrentCSVWriter.writerow([ClubNumber, CharterDate, Website, Facebook, MeetingTimes, Location, Restrictions])

Log("Collected club data")

OpenCurrentFile.close()
OpenClubNumberFile.close()

EndTime = datetime.now() 
Log("Time Taken: " + str(EndTime - StartTime))