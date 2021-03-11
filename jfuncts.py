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

def getZipJobs(url):
    joblist = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    result = soup.find(id='job_results')
    print(result)
    jobs = result.find_all('article', class_='quiz-card-')
    for s_job in jobs:
        title = s_job.find('h2', class_='job_title')
        company = s_job.find(class_='job_org')
        if None in (title, company):
    	    continue
        print(company.text.strip())
        print(title.text.strip())
    return joblist
