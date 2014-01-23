# importing all the libraries required by this program
from bs4 import BeautifulSoup as bs
from urllib import urlopen
import writetocsv

baseurl = "http://www.healthkart.com"
# the category url's we need to hit
categories = ["/fitness?navKey=CP-sv-fitness&itracker=w:emenu|;p:1|;c:fitness|;",
			  "/sports?navKey=CP-sv-sport&itracker=w:emenu|;p:1|;c:sports|;"]
# array that we will fill up with sub category links
sub_category = []


# function to retrieve products from provided
def get_product_links(url,page=1,flag=1):
  print "on page -> %d" % page
  cat = bs(urlopen(url).read())
  # for all product found on page
  for prod in cat.find_all(class_="varnt-cont"):
    # check to see if it is in stock
    outofstock = prod.find(class_="oos-cntnr")
    if not outofstock:
      # retrieve product details
      prod_url = prod.find(class_="mrgn-t-10").find('a').get('href')
      prod_name = prod.find(class_="mrgn-t-10").find('a').text.strip()
      prod_price = prod.find(class_="final-price").text.strip()
      # check to see if product is a duplicate
      if not prod_url in product_links:
        # append product to products array
        product_links.append(prod_url)
        products.append([prod_url,prod_name,prod_price])
      else:
        print "Duplicate product"
    else:
      flag = 0
      break
  if flag:
    # check if there is a next page for the product
    try:
      page+=1
      # call the function recursively
      get_product_links(baseurl+cat.find('a',class_="btn").get('href'),page)
    except Exception:
      print "last page reached"
  else:
    # dont go to next page when out of stock reached as all products after this are out of stock
    print "outofstock reached"


# hit the required categories and retrieve subcat links
for category in categories:
  cat = bs(urlopen(baseurl+category).read())
  sub_category.extend([[a.text,a.get('href')] for a in cat.find(class_="menu-content").find(class_="gl").find_all(class_="sc-cat-nm")])


product_links = []
products = []

# hit all subcats and get products
for category in sub_category:
  print "going into -> %s" % category[0]
  get_product_links(category[1])

#save the product array to a csv file
writetocsv.write_to_file(products,"healthkart")