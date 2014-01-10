#!/usr/bin/env from

from urllib import urlopen, urlencode
import csv
import re
from bs4 import BeautifulSoup as bs
def get_fields(page):
    hiddens = page.findAll('input')
    fields = {}
    for b in hiddens:
        # get all hidden input fields that are not prodname
        if(b.get('type')=='hidden'):
		  fields[str(b.get('name'))] = "" if (str(b.get('name'))=="prodname") or (str(b.get('value'))=="None") else str(b.get('value'))
    return fields

def get_links(page):
    # clubbing the related data together with zip function into new array
    links = zip(page.findAll(class_='browseSkuName'),page.findAll(class_="browsePrice"))
    # get the 3 required fields into an array
    return [[b[0].findAll('a')[0].get('href'),b[0].findAll('a')[0].get_text(),b[1].get_text()] for b in links]

# The Categories that we want to loop through
categories = ["Fitness","Sports"]
for category in categories:
    # The url from which we need to pick up the products
    url = "http://www.playgroundonline.com/%s" % category
    # open the url and pass it to Beautiful Soup for parsing
    homepage = bs(urlopen(url).read())
    # These fields are required for the post request else the result will be blank - Not good
    fields = get_fields(homepage)
    # This is the data that we want to store in the CSV file
    links = get_links(homepage)
    # count of the pages
    currentpage = 1
    # number of pages that we will paginate
    pages = int(fields["ctl00$ContentPlaceHolder1$product_list_inc$hPageCount"])
    while currentpage<pages:
        currentpage +=1
        # set the page in the post params to the current page
        page = "ctl00$ContentPlaceHolder1$product_list_inc$link2%d" % currentpage
        # post params other than those from the get_fields function
        params1 = {"ctl00$ScriptManager1":"ctl00$ContentPlaceHolder1$product_list_inc$UpdatePanel1|%s" % page, "ctl00_ScriptManager1_HiddenField":";;AjaxControlToolkit, Version=1.0.20229.20821, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:c5c982cc-4942-4683-9b48-c2c58277700f:e2e86ef9:1df13a87:3858419b:9ea3f0e2:96741c43:c4c00916:c7c04611:cd120801:38ec41c0", "__EVENTTARGET":"%s" % page, "__EVENTARGUMENT":"", "__LASTFOCUS":"", "__VIEWSTATE": str(fields["__VIEWSTATE"]), "ctl00$Search_block1$txtsrchInDesc":"", "ctl00$Search_block1$ddlCategory":"", "ctl00$ContentPlaceHolder1$product_list_inc$hdnprodid":"", "ctl00$ContentPlaceHolder1$product_list_inc$hdnValidateEmailId":"", "ctl00$ContentPlaceHolder1$product_list_inc$hidCheckedProducts":"", "ctl00$ContentPlaceHolder1$product_list_inc$hdnSrchPagesIndex":"", "ctl00$ContentPlaceHolder1$product_list_inc$ddlSrchPages":"20", "ctl00$ContentPlaceHolder1$product_list_inc$ddlSrchPages1":"20", "ctl00$ContentPlaceHolder1$product_list_inc$hIsScm":"0", "ctl00$ContentPlaceHolder1$product_list_inc$hScmSort":"", "ctl00$ContentPlaceHolder1$product_list_inc$hOrderBy":"", "ctl00$ContentPlaceHolder1$product_list_inc$hCurrentPage":"0", "ctl00$ContentPlaceHolder1$product_list_inc$hViewAll":"False", "ctl00$ContentPlaceHolder1$product_list_inc$hPageCount":str(pages), "ctl00$ContentPlaceHolder1$product_list_inc$hddlsrch":"20", "ctl00$ContentPlaceHolder1$product_list_inc$hddlsrch1":"20", "ctl00$ContentPlaceHolder1$product_list_inc$txtEmail":""}
        # combine the post params and encode them for post
        params = urlencode(dict(params1.items() + fields.items()))
        # fetch the next page with the post request and pass it to Beautiful Soup
        innerpage = bs(urlopen(url+"?name1=Sports&lvl=0&type=categories",params).read())
        # add new data to the links array
        links.extend(get_links(innerpage))
        # get fields required for next post request
        fields = get_fields(innerpage)
        # show progress to the user
        print "going to page number %d" % currentpage
    # open new file for dumping the colleted data
    with open('dump'+category+'.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for link in links:
            # convert each field to utf-8 so that special characters are not lost
            link=[s.encode('utf-8') for s in link]
    	    spamwriter.writerow(link)
