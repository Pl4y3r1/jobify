import requests
import argparse
import os
import sys
from jfuncts import *
from bs4 import BeautifulSoup

indJobs = []
monJobs = []
zipJobs = []

parser = argparse.ArgumentParser(description='Job Title and Location')
parser.add_argument('Title', metavar='title', nargs='+', type=str, help='The tile of the job you want to search for')
parser.add_argument('Location', metavar='location', nargs='+', type=str, help='The location you want to search in')
args = parser.parse_args()

url = 'https://www.monster.com/jobs/search/?q=' + ' '.join(args.Title) + '&where=' + ' '.join(args.Location) + '&stpage=1&page=10'
monJobs = getMonsterJobs(url)

url = 'https://www.ziprecruiter.com/candidate/search?search=' + ' '.join(args.Title) + '&location=' + ' '.join(args.Location) + '&__cf_chl_captcha_tk__=114f9c9f4ebbc8a695018ffeb65c47388e3cf0e0-1615435883-0-ASuSx6rQFLrC1KJVBZOYFtbuQdlarqRpSJMaao5b326FUQK_Zu9pgizd-979DOI53FWyU94X1rqHA_O98URu5wxycMZrTy5oDxbiZcC7PE3zzqG6JHUAfvGR_h0AR1YoBTv5w6_Pv7CNoZrAo0ldOHdo6Je1lapOh5itCMhCh26IKWZj75oxyWCb38pr6REBJ0A7RkNqR-5Mn1rbi5dSDfwuqkd6QwrmaD9wEKW9c1JuPmSnGzYQICB0_PKQLhdycG3Xgx6aKaRTP_Q2Mj1xmhJPIgzBLxlRuBziLhzoEBOmyGaF9VJkBGbFYjxwrjDcoqmKyxGIRNWejiNdfH6KK5bIxFna1x4KpS8y8pfWSMsewt6gAbN_zOgBlbFqlDNvvkOFCZnLiGAI052L4qu3VdzxT-yKivMfTimrMNXxcFTTrGcRhC0tMZC1dO5VNjc10M2brXto_fdszCsdOXoIsYVqFvyiIqeprphrrZbs2lc61zowvGX12FQNk5t9xgVrs0KmZk8_o4QUR9Y89iVg2m-Y1JSgDE3S06UXl8ARrKkMqSPH-lY2QWs9Oh2GOcL_fv8rtpHf6xQjr7pXIQi19W-RiJfyMtMsiUcn4zptdfBrrTVbi2fyj2llyC8d47gqpZqlVVwqouaNv9b68s44MwQ&page=6'
zipJobs = getZipJobs(url)

i = 0
while i < 10:
    url = "https://www.indeed.com/jobs?q=" + " ".join(args.Title) + "&l=" + " ".join(args.Location) + "&start=" + str(i)
    indJobs = indJobs + getIndeedJobs(url)
    i += 1

for s_job in monJobs:
    s_job.printData()
    print('\n')
for s_job in indJobs:
    s_job.printData()
    print('\n')
for s_job in zipJobs:
    s_job.printData()
    print('\n')

print("Number of total Jobs")
print(len(monJobs) + len(indJobs))
