import argparse
import requests
from bs4 import BeautifulSoup
import json
import math
import re
import pandas as pd 

def load_url(link, job, location):
    if option.url == 'seek':
        url = link + job + '-jobs/in-'+ location + '?sortmode=ListedDate'
    else:
        url = link
    print (url)
    return url

def next_page(link, page_no):
    if option.url == 'seek':
        url = link + '&page=' + str(page_no)
    else:
        url = link
    return url

def no_of_jobs(job_ad_summary):
    a = job_ad_summary['data-sol-meta']
    a = json.loads(a)
    tot_size = int(a['totalJobCount'])
    per_page = int(a['pageSize'])
    tot_pages = int(tot_size/per_page)
    return tot_size,per_page,tot_pages

def extract_title(job_ads):
    a = job_ads.find('article',{'aria-label': True})
    return a['aria-label']

def extract_company(job_ads):
    a = job_ads.find('a',{'class': '_3AMdmRg'})
    return a.string

def extract_location(job_ads):
    a = job_ads.find('strong', {'class': 'lwHBT6d'})
    a = a.find('a',{'class': '_3AMdmRg'})
    return a.string

def job_link(job_ads):
    link = []
    des = []
    no_des = []
    url = 'https://www.seek.com.au'
    for job in job_ads:
        s = ()
        a = job.find("span",{"class": "_3FrNV7v _2IOW3OW HfVIlOd _2heRYaN E6m4BZb"})
        a = a.find("a",{"class": "_2iNL7wI"})
        l = url +a['href']
        link.append(url +a['href'])
        t = extract_job_description(l)
        title = extract_title(job)
        company = extract_company(job)
        loc = extract_location(job)
        s = (title,company,loc,l)
        if (option.citizen == True) and (rem(title.lower()) == False):
            des.append(s)
        else:
            if (t == False) and (rem(title.lower()) == False):
                des.append(s)
            else:
                no_des.append(s)
    return des, no_des

def check(sentence, words): 
    res = [] 
    for substring in sentence: 
        k = [ w for w in words if w in substring ] 
        if (len(k) == len(words) ): 
            res.append(substring)
    return (res)

def extract_job_description(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    a = soup.find("div", {"class": "_2e4Pi2B"})
    a = a.text
    #aus = ['Australian Citizen', 'Australian citizen', 'Australian Citizens', 'Australian citizens']
    if 'Australian Citizen' in a or 'Australian citizen' in a or 'Australian Citizens' in a or 'Australian citizens' in  a or 'citizenship' in a or 'Citizenship' in a:
        return True
    else:
        return False

def rem(job_ads):
    if any(word in job_ads for word in option.ignore):
        return True
    else:
        return False

def flatten(x):
    result = []
    for l in x:
        for el in l:
            result.append(el)
    return(result)
        

def main():
    for feild in option.feilds:
        if option.url == 'seek':
            url = 'https://www.seek.com.au/'
            url = load_url(url,feild, option.location)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            job_soup_summary = soup.find("div", {"id": "searchResultSummary"})
            print(url)
            a,b, tot_pages = no_of_jobs(job_soup_summary)
            pages = int(int(option.pages)*tot_pages/100)
            print(pages)
            i = 1
            link = url
            dest = []
            no_dest = []
            while i <= pages:
                page = requests.get(link)
                soup = BeautifulSoup(page.content, "html.parser")
                job_soup = soup.find_all("div", {"data-search-sol-meta":True})
                des, no_des = job_link(job_soup)
                dest.append(des)
                no_dest.append(no_des)
                i+=1
                link = next_page(url,i)
            dest = flatten(dest)
            no_dest = flatten(no_dest)
            file_name_dest = feild+'_apply.csv'
            file_name_no_dest = feild + '_no_apply.csv'
            if len(no_dest) == 0:
                df_dest = pd.DataFrame(dest)
                df_dest.to_csv(file_name_dest)
            else:
                df_dest = pd.DataFrame(dest)
                df_no_dest = pd.DataFrame(no_dest)
                df_dest.to_csv(file_name_dest)
                df_no_dest.to_csv(file_name_no_dest)
            print (df_dest)
            print (df_no_dest)
        elif option.url == 'indeed':
            print('no')
        elif option.url == 'jora':
            print('jora')
        else:
            print('no')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', default='seek')
    parser.add_argument('-feilds', default= ['mechatronics-engineering'])
    parser.add_argument('-location', default='All-Australia')
    parser.add_argument('-pages', default='50')
    parser.add_argument('-ignore', default= ["senior", "intern", "contract", "staff"])
    parser.add_argument('-citizen', default= False)
    option = parser.parse_args()
    main()