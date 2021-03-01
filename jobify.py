import requests
import argparse
import os
import sys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Job Title and Location')

parser.add_argument(
    'Title', metavar='title', nargs='+', type=str, help='The title of the job you want to search for')
parser.add_argument(
    'Location', metavar='location', nargs='+', type=str, help='The location you want to search in')

args = parser.parse_args()

url1 = 'https://www.monster.com/jobs/search/?q=' + \
    ' '.join(args.Title) + '&where=' + \
    ' '.join(args.Location) + '&stpage=1&page=10'

url2 = 'https://www.indeed.com/jobs?q=' + \
    ' '.join(args.Title) + '&l=' + ' '.join(args.Location) + '&start=0'

page1 = requests.get(url1)
page2 = requests.get(url2)

soup1 = BeautifulSoup(page1.content, 'html.parser')
soup2 = BeautifulSoup(page2.content, 'html.parser')

results1 = soup1.find(id='ResultsContainer')
results2 = soup2.find(id='resultsCol')

jobs1 = results1.find_all('section', class_='card-content')
jobs2 = results2.find_all('div', class_='jobsearch-SerpJobCard')

searched_jobs1 = results1.find_all(
    'h2', string=lambda text: ' '.join(args.Title))
searched_jobs2 = results2.find_all(
    'h2', string=lambda text: ' '.join(args.Title))

print("Number of " + ' '.join(args.Title) + " Jobs Found")
print(len(searched_jobs1))

for s_job in jobs1:
    title = s_job.find('h2', class_='title')
    company = s_job.find('div', class_='company')
    if None in (title, company):
        continue
    link = s_job.find('a')['href']
    print(title.text + company.text)
    print(link)
for s_job in jobs2:
    title = s_job.find('h2', class_='title')
    company = s_job.find(class_='company')
    if None in (title, company):
        continue
    link = s_job.find('a')['href'].replace("/rc/clk?", "")
    link = link.split("id", 1)[0]
    print(title.text + company.text)
    if "company" in link:
        print(f"https://www.indeed.com{link}")
    if "pagead" in link:
        print(f"https://www.indeed.com{link}")
    else:
        print(f"https://www.indeed.com/viewjob?{link}")

print("Number of " + ' '.join(args.Title) + " Jobs Found")
print(len(searched_jobs1) + len(searched_jobs2))
print("Number of total Jobs")
print(len(jobs1 + jobs2))
# print(results2.prettify())
