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
urllist = []

i = 0
while i < 10:
    urllist.append("https://www.indeed.com/jobs?q=" + " ".join(args.Title) + "&l=" + " ".join(args.Location) + "&start=" + str(i))
    i += 1

pagelist = []

page1 = requests.get(url1)

i = 0
while i < 10:
    pagelist.append(requests.get(urllist[i]))
    i += 1

soup1 = BeautifulSoup(page1.content, 'html.parser')
souplist = []

i = 0
while i < 10:
    souplist.append(BeautifulSoup(pagelist[i].content, 'html.parser'))
    i += 1

results1 = soup1.find(id='ResultsContainer')
resultlist = []

i = 0
while i < 10:
    resultlist.append(souplist[i].find(id='resultsCol'))
    i += 1

jobs1 = results1.find_all('section', class_='card-content')
jobslist2 = []

i = 0
while i < 10:
    jobslist2.append(resultlist[i].find_all('div', class_='jobsearch-SerpJobCard'))
    i += 1

i = 0
jobslist3 = []
while i < 10:
    jobslist3 = jobslist3 + jobslist2[i]
    i += 1

searched_jobs1 = results1.find_all(
    'h2', string=lambda text: ' '.join(args.Title))
#searched_jobs2 = results2.find_all(
#    'h2', string=lambda text: ' '.join(args.Title))

for s_job in jobs1:
    title = s_job.find('h2', class_='title')
    company = s_job.find('div', class_='company')
    if None in (title, company):
        continue
    link = s_job.find('a')['href']
    print(title.text + company.text)
    print(link)

for s_job in jobslist3:
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

print("Number of " + ' '.join(args.Title) + " Jobs Found on Monster")
print(len(searched_jobs1))
print("Number of total Jobs")
print(len(jobs1) + len(jobslist3))
