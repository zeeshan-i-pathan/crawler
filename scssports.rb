require 'nokogiri'
require 'open-uri'
output = ""
newproduct = ""
puts "Opening Homepage"
# Visiting home page of the website
homepage = Nokogiri.HTML(open("http://www.scssports.in"));1
links = []
# Collecting all the categories from the navigation and making an hash array from them
# In the hash parent is the category name and link is the link to the category we'll need these details later
links = homepage.css('#menu ul li ul li a').collect{|x| {:parent => x.text, :link => x['href']} }

def openpage(link)
  # visiting the link passed - getting 100 products at a time the max allowed per page for this site
  page = Nokogiri.HTML(open(link[:link]+"&limit=100"));1
  products ||= []
  # putting all the product url's into the products array
  products << page.css('.box-product-item .image a').collect{|x| x[:href]};1
  begin
    # recursively going through the pagination until there is no more last page
    # in that case the rescue block will be called
  	nextpage = {:link => page.css('.pagination .links a')[-2][:href], :parent => link[:parent]}
  	products << openpage(nextpage)
  rescue
  end
  # return products array once all the products have been retrieved
  products
end

class String
  def price_trim
    self.gsub("Rs","").gsub(". ","").gsub(',','')
  end
end
# Opening the previous csv file that we wrote to that contains products already in the system
file = File.open "scssports.csv"
# Reading this file and putting the product urls into the visitedProducts array
visitedProducts=[]; CSV.parse(file) {|x| visitedProducts << x[-1]; output << x.to_s << "\n" }
# Looping through each category
links.each do |link|
  # getting all product urls from each category - see openpage function
  allproducts = openpage(link).flatten!
  # looping through all the products returned by the above script
  allproducts.each do |product|
    # if product url already visited in a previous read skip it
  	unless visitedProducts.include? product
      puts "Adding product..."
      # visiting the new products url
      page = Nokogiri.HTML(open(product));1
  	  # retriving the required fields
      product_id = page.css('input[type="hidden"]').first['value']
  	  title = page.css('#content h1').first.text
  	  category = link[:parent]
  	  item_code = page.css('.description').text.split(':')[2].gsub("Availability","").strip!
      # not all products have this field there the begin - rescue
      begin
        mrp_price = page.css('.product-info .price .price-old').text.price_trim
      rescue
      end
      # not all products have this field there the begin - rescue
      begin
        dis_price = page.css('.product-info .price .price-new').text.price_trim
      rescue
      end
  	  image = page.css('.product-info .image a').first[:href]
  	  description =  page.css('#tab-description').first.content.gsub("\"","")
      # put the fields into the csv format
      str = ["\"#{category}\"","\"#{title}\"","\"#{item_code}\"","\"#{mrp_price}\"","\"#{dis_price}\"","\"#{description}\"","\"#{image}\"","\"#{product}\""].join(",")
      # append the new products to the existing product list
      output << str << "\n"
      # make a list of the new products
      newproduct << str << "\n"
    end
  end
end
# write the existing product list back to the csv file
# This will be needed for the next crawl
File.open("scssports.csv","w"){|f|f.write output}
# write the new products to the csv that will be used by the sites upload script
File.open("scssports-newproducts.csv","w"){|f|f.write newproduct}