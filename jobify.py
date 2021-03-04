import requests
import argparse
import os
import sys
from bs4 import BeautifulSoup

class JOB:
    def __init__(self, title, company, link):
        self.title = title
        self.company = company
        self.link = link

    def printData(self):
        print("Title: " + str(self.title))
        print("Company: " + str(self.company))
        print("Link: " + str(self.link))

def getMonsterJobs(url):
    joblist = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    jobs = results.find_all('section', class_='card-content')
    for s_job in jobs:
        title = s_job.find('h2', class_='title')
        company = s_job.find('div', class_='company')
        if None in (title, company):
            continue
        link = s_job.find('a')['href']
        joblist.append(JOB(title.text.strip(), company.text.strip(), link))

    return joblist

parser = argparse.ArgumentParser(description='Job Title and Location')
parser.add_argument('Title', metavar='title', nargs='+', type=str, help='The tile of the job you want to search for')
parser.add_argument('Location', metavar='location', nargs='+', type=str, help='The location you want to search in')
args = parser.parse_args()

url = 'https://www.monster.com/jobs/search/?q=' + \
    ' '.join(args.Title) + '&where=' + \
    ' '.join(args.Location) + '&stpage=1&page=10'
urllist = []
monJobs = getMonsterJobs(url)

i = 0
while i < 10:
    urllist.append("https://www.indeed.com/jobs?q=" + " ".join(args.Title) + "&l=" + " ".join(args.Location) + "&start=" + str(i))
    i += 1

pagelist = []

i = 0
while i < 10:
    pagelist.append(requests.get(urllist[i]))
    i += 1

souplist = []

i = 0
while i < 10:
    souplist.append(BeautifulSoup(pagelist[i].content, 'html.parser'))
    i += 1

resultlist = []

i = 0
while i < 10:
    resultlist.append(souplist[i].find(id='resultsCol'))
    i += 1

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

#searched_jobs1 = results1.find_all(
#    'h2', string=lambda text: ' '.join(args.Title))
#searched_jobs2 = results2.find_all(
#    'h2', string=lambda text: ' '.join(args.Title))

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
    elif "pagead" in link:
        print(f"https://www.indeed.com{link}")
    else:
        print(f"https://www.indeed.com/viewjob?{link}")
for s_job in monJobs:
    s_job.printData()
    print('\n')

print("Number of total Jobs")
print(len(monJobs) + len(jobslist3))
