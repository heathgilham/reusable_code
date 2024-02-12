import requests
from lxml import html
import csv
import datetime
import os
import pandas as pd
from urllib.parse import urljoin

os.chdir(os.path.dirname(__file__))

# URLs to scrape
urls = [
    ("https://www.volunteer.com.au/volunteering/in-melbourne-cbd-inner-suburbs-melbourne-vic?radius=5&typeofwork=2%2C3%2C4%2C8%2C9%2C10%2C11%2C13%2C14%2C16%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C27%2C28%2C30", '//div[1]/main/section/div[2]/section/ul/li/article/header/h3/a', '//div[1]/main/section/div[2]/section/ul/li/article/header/h4/a'),
    ("https://www.volunteer.com.au/volunteering/in-online-or-remote?radius=5&typeofwork=2%2C3%2C4%2C8%2C9%2C10%2C11%2C13%2C14%2C16%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C27%2C28%2C30", '//div[1]/main/section/div[2]/section/ul/li/article/header/h3/a', '//div[1]/main/section/div[2]/section/ul/li/article/header/h4/a'),
    ("https://govolunteer.com.au/volunteering/in-melbourne-city?cause=14%2c24%2c18%2c21%2c5%2c13%2c16%2c23%2c8%2c25%2c17%2c9%2c2&interest=23%2c28%2c9%2c4%2c18%2c16%2c22%2c27%2c8%2c21&youravailability=3%2c5", '//div[1]/div/div/div[2]/fieldset/ol/li/div[1]/header/h2/a', '//div[1]/div/div/div[2]/fieldset/ol/li/div[1]/header/p/strong'),
    ("https://www.ethicaljobs.com.au/jobs?categories=54%2C16%2C29%2C34%2C36%2C39%2C42%2C45%2C51%2C53&workTypes=6", '//div[1]/div[3]/main/section[2]/div/div/div[1]/a/div[1]/div[1]/h2', '//div[1]/div[3]/main/section[2]/div/div/div[1]/a/div[1]/div[1]/div')
    # ("https://probonoaustralia.com.au/search-opportunity/?pages=2&type=volunteer&q&tax_input%5Bsector%5D%5B0%5D&tax_input%5Bprofession%5D%5B0%5D&tax_input%5Blocation%5D%5B0%5D","/html/body/div[1]/div[11]/div/div[4]/div[4]/div[1]/div/div[2]/div/h3/a","/html/body/div[1]/div[11]/div/div[4]/div[4]/div[3]/div/div[2]/div/div[1]/span[1]")
]

# List of organisations to ignore
filter_words = ['cricket', 'jazz', 'catholic', 'animal', 'climate', 'jewish', 'toy library', 'planetary healing', 'church', 'christ', 'dcss australia', 'epilepsy', 'soccer', 'foxg1', 'furry', 'get 2 know', 'girl guides', 'inclusion melbourne', 'Inspiring Girls Australia', 'islam', 'LINK Community & Transport', 'Melbourne Adult Migrant English Program (AMEP)', 'Mentoring Men', 'Mission to Seafarers Victoria', 'MS Plus', 'russian', 'NFPCCC', 'rspca', 'sudanese', 'scientology', 'Southern Migrant & Refugee Centre(SMRC)', 'special olympics', 'dogs']  # Replace with the words you want to filter


def get_new_volunteer_roles(url, role_xpath, org_xpath):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    tree = html.fromstring(response.content)
    new_roles = []
    for role, organisation in zip(tree.xpath(role_xpath), tree.xpath(org_xpath)):
        organisation_name = organisation.text_content().strip()
        if any(word.lower() in organisation_name.lower() for word in filter_words):
            continue  # Skip this role if the organisation is in the ignore list
        title = role.text_content().strip()
        role_url_relative = role.get('href')
        role_url = urljoin(url, role_url_relative)  # Convert relative URL to absolute URL
        new_roles.append((title, organisation_name, role_url))
    return new_roles

def write_to_csv(new_roles):
    date_checked = datetime.datetime.now().strftime('%Y-%m-%d')
    headers = ['Date Checked', 'Role Title', 'Organisation Name', 'URL']
    new_data = pd.DataFrame([(date_checked, title, org, url) for title, org, url in new_roles], columns=headers)
    if os.path.exists('volunteer_roles.csv'):
        existing_data = pd.read_csv('volunteer_roles.csv')
        data = pd.concat([existing_data, new_data]).drop_duplicates(subset=['Role Title', 'Organisation Name', 'URL'])
    else:
        data = new_data
    data.to_csv('volunteer_roles.csv', index=False)

for url, role_xpath, org_xpath in urls:
    page_number = 1
    while True:
        url_with_page = url + f"&page={page_number}"
        new_roles = get_new_volunteer_roles(url_with_page, role_xpath, org_xpath)
        if not new_roles:   
            break  # Exit loop if no more roles are found
        write_to_csv(new_roles)
        page_number += 1  # Increment the page number for the next iteration