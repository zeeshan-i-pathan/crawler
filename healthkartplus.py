#!/usr/bin/env from

from urllib import urlopen, urlencode
import csv
import re
from bs4 import BeautifulSoup as bs

url = "http://www.healthkartplus.com/pharmaceutical-companies.html"
homepage = bs(urlopen(url).read())
parentsite = "http://www.healthkartplus.com"
# get all the pharmaceutical companies of india
# left side
companies = [[name.text,parentsite+name.get('href')] for name in homepage.find_all(class_='leftColManu')[0].find_all('a')]
# right side
right = [name.find_all('a') for name in homepage.find_all(class_="rightColManu")]
right.pop()
companies.extend([[name[0].text,parentsite+name[0].get('href')] for name in right])
# list to maintain names of drugs
drugs = []
# write the companies that are found to a file
write_to_file(companies,"companies")
for company in companies:
  print "looping through %s" % company[0]
  companypage = bs(urlopen(company[1]).read())
  drugs.extend([[drug.text,drug.get('href'),company[0]] for drug in companypage.find_all(class_="columnMedList")[0].find_all('a')])
# write the drugs that are found to a file
write_to_file(drugs,"drugs")
drugdetail = []
salts = []
for drug in drugs:
  print "checking out %s" % drug[0]
  page = bs(urlopen(parentsite+drug[1]).read())
  try:
    saltname = page.find(class_="sltNm").find_all('a')
    for salt in saltname:
      if not salt.text in salts:
        salts.append(salt.text)
    saltname = ",".join([name.text.encode('utf-8') for name in saltname])
    medtype = page.find(class_="mdcnNm").find('img').get('src').split("/")[-1].split('.')[0]
    size = page.find(class_="sizDtl").text
    company = page.find(class_="mfgNm").text.strip()
    drugdetail.append([drug[0],medtype,size,saltname,company])
  except Exception:
  	print "%s Not a normal medican" % drug[0]

def write_to_file(array,name):
  with open(name+".csv","wb") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for element in array:
      element = [s.replace("\n","").encode('utf-8') for s in element]
      spamwriter.writerow(element)