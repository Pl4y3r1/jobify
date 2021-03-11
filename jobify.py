import requests
import argparse
import os
import sys
from jfuncts import *
from bs4 import BeautifulSoup

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
