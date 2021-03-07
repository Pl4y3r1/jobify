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

def getIndeedJobs(url):
    joblist = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(id='resultsCol')
    jobs = result.find_all('div', class_='jobsearch-SerpJobCard')
    for s_job in jobs:
        title = s_job.find('h2', class_='title')
        company = s_job.find(class_='company')
        if None in (title, company):
            continue
        link = s_job.find('a')['href'].replace("/rc/clk?", "")
        link = link.split("id", 1)[0]
        if "company" in link:
            link = "https://www.indeed.com" + link
            joblist.append(JOB(title.text.strip(), company.text.strip(), link))
        elif "pagead" in link:
            link = "https://www.indeed.com" + link
            joblist.append(JOB(title.text.strip(), company.text.strip(), link))
        else:
            link = " https://www.indeed.com/viewjob?" + link
            joblist.append(JOB(title.text.strip(), company.text.strip(), link))
    return joblist

parser = argparse.ArgumentParser(description='Job Title and Location')
parser.add_argument('Title', metavar='title', nargs='+', type=str, help='The tile of the job you want to search for')
parser.add_argument('Location', metavar='location', nargs='+', type=str, help='The location you want to search in')
args = parser.parse_args()

url = 'https://www.monster.com/jobs/search/?q=' + ' '.join(args.Title) + '&where=' + ' '.join(args.Location) + '&stpage=1&page=10'
urllist = []
indJobs = []
monJobs = getMonsterJobs(url)

i = 0
while i < 10:
    url = "https://www.indeed.com/jobs?q=" + " ".join(args.Title) + "&l=" + " ".join(args.Location) + "&start=" + str(i)
    indJobs = indJobs + getIndeedJobs(url)
    i += 1

#searched_jobs1 = results1.find_all(
#    'h2', string=lambda text: ' '.join(args.Title))
#searched_jobs2 = results2.find_all(
#    'h2', string=lambda text: ' '.join(args.Title))

for s_job in monJobs:
    s_job.printData()
    print('\n')
for s_job in indJobs:
    s_job.printData()
    print('\n')

print("Number of total Jobs")
print(len(monJobs) + len(indJobs))
