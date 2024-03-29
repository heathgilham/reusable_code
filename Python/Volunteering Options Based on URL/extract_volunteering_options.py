# Purpose: Create list of volunteering opportunities
# Author: Heath Gilham
# Logic: Download HTML from websites based on filters. Find roles and link based on class / href tag. Export roles to file for those which haven't already been checked.
# Instructions: 1. Install the latest version of Python 3 - https://www.python.org/downloads/
#               2. Go to each website and select relevant filters to get the relevant URL for use below on row 58, 88 & 118
#               3. Run in python intepreter
#				4. Check through whole list and copy link into chrome if interested

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

# Define Variables
os.chdir(os.path.dirname(__file__))
StartTime = datetime.now() 
Datetime = datetime.now().strftime("%d%m%Y_%I%M%p")
Date = datetime.now().strftime("%d-%m-%Y")
DateForFile = datetime.now().strftime("%d/%m/%Y %I:%M:%S%p")
LogFolder = "Log/"
LogFile = LogFolder + "/" + Date + ".log"
IsDebuggingMode = False
OldFileDirName = "Old_files"
CSVExportFile = "volunteer_options.csv"
CSVCheckedFile = "volunteer_options_checked.csv"
CurrentCheckedLinks = []
if not os.path.exists(LogFolder):  os.makedirs(LogFolder)
if not os.path.exists(LogFile):  open(LogFile,"w")
if not os.path.exists(CSVCheckedFile): csv.writer(open(CSVCheckedFile,'w', encoding="utf-8"), quoting=csv.QUOTE_ALL).writerow(["Date Checked","Role","Link"])
OpenCurrentFile = open(CSVCheckedFile,'a', newline='', encoding="utf-8")
CurrentCSVWriter = csv.writer(OpenCurrentFile, quoting=csv.QUOTE_NONE, escapechar=';')

PreviousCheckedLinks = [line[2] for line in csv.reader(open(CSVCheckedFile, "r", encoding="utf-8", errors="ignore"))]
           
Log("Running " + os.path.basename(sys.argv[0]))

# Log("Collecting EthicalJobs data")

# srcdata = requests.get(r"https://www.ethicaljobs.com.au/jobs?categories=54%2C16%2C29%2C34%2C36%2C39%2C42%2C45%2C51%2C53&workTypes=6").content
# ATags = BeautifulSoup(srcdata, features = "html.parser").find_all("a")

# for tag in ATags:
    
#     try:
#         TagClass = tag.attrs['class']
#     except:
#         TagClass = ""
    
#     if "Tilestyles__TileContainer-sc-14evrxc-1" in TagClass:
#         href = tag.attrs['href']
#         URL = "https://www.ethicaljobs.com.au" + href
#         URL = URL.split('?')[0]
        
#         if URL not in PreviousCheckedLinks and URL not in CurrentCheckedLinks:
#             print(URL)
#             print(tag.text.replace(",",";").replace('"',";").replace('\n',"").replace("•","").rstrip())
#             CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";").replace('"',";").replace('\n',"").replace(" "," ").rstrip(), URL])
#             CurrentCheckedLinks += [URL]
   
# Log("New EthicalJobs roles added to csv")


Log("Collecting Volunteer.com.au in person data")

headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

rolesperpage = 15               
rolecount = 15 
pagenum = 0              
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://www.volunteer.com.au/volunteering/in-melbourne-cbd-inner-suburbs-melbourne-vic?page=" + str(pagenum) + r"&radius=5&typeofwork=2%2C3%2C4%2C8%2C9%2C10%2C11%2C13%2C14%2C16%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C27%2C28%2C30", headers=headers).content
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
                CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";").replace('"',";"), URL])
                CurrentCheckedLinks += [URL]
    
Log("New Volunteer.com.au in person roles added to csv")


Log("Collecting Volunteer.com.au online data")

rolesperpage = 15
rolecount = 15
pagenum = 0
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://www.volunteer.com.au/volunteering/in-online-or-remote?page=" + str(pagenum) + r"&radius=5&typeofwork=2%2C3%2C4%2C8%2C9%2C10%2C11%2C13%2C14%2C16%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C27%2C28%2C30", headers=headers).content
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
                CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";"), URL])
                CurrentCheckedLinks += [URL]
   
Log("New Volunteer.com.au online roles added to csv")


Log("Collecting GoVolunteer data")

rolesperpage = 20               
rolecount = 20 
pagenum = 0               
while rolecount == rolesperpage:
    pagenum += 1
    srcdata = requests.get(r"https://govolunteer.com.au/volunteering/in-melbourne-city?cause=14%2c24%2c18%2c21%2c5%2c13%2c16%2c23%2c8%2c25%2c17%2c9%2c2&interest=23%2c28%2c9%2c4%2c18%2c16%2c22%2c27%2c8%2c21&page=" + str(pagenum) + r"&youravailability=3%2c5").content
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
                CurrentCSVWriter.writerow([DateForFile, tag.text.replace(",",";"), URL])
                CurrentCheckedLinks += [URL]
                    
Log("New GoVolunteer roles added to csv")

OpenCurrentFile.close()
EndTime = datetime.now() 
Log("Time Taken: " + str(EndTime - StartTime))
