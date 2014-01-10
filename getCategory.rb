require 'nokogiri'
require 'open-uri'
  output = ""
  link = ARGV[0]
  index = ARGV[1]
  puts "link is #{link}"
  page = Nokogiri.HTML(open(link));1
	begin
		pages = page.css('.pagination').first.css('a').collect{|x| "http://www.gofitindia.com/"+x['href']}
	rescue
		pages = []
	end
	puts "There were #{pages.count} pages"
  products = []
  products << page.css('.product-container').collect{|x| "http://www.gofitindia.com/"+x.css('a').first['href']}
	puts "Going through each page"
  pages.each do |paginate|
    page = Nokogiri.HTML(open(paginate));1
    products << page.css('.product-container').collect{|x| "http://www.gofitindia.com/"+x.css('a').first['href']}
  end
  products.flatten!
	puts "Found #{products.size} products"
  products.each do |product|
		puts "Adding product..."
    page = Nokogiri.HTML(open(product));1
    product_id = product.split("=").last
    category = page.css('.breadcrumbs a').last.text.gsub("\"","")
    title = page.css('.mainbox-title').text.gsub("\"","")
    item_code = page.css('.shippingprice').first.text.split(":").last.gsub(/\s+/,'')
		begin
			mrp_price = page.css('.list-price').select{|x| x['id']=="sec_list_price_#{product_id}"}.first.text.gsub("\"","")
		rescue
		end
		begin
			dis_price = page.css('.price').select{|x| x['id']=="sec_discounted_price_#{product_id}"}.first.text.gsub("\"","")
		rescue
		end
		description = page.css('.wysiwyg-content').select{|x| x["id"]=="content_block_description" }.first.content.gsub("\"","")
    image = "http://www.gofitindia.com/"+page.css('.center').select{|x| x["id"]=="detailed_box_#{product_id}"}.first.css('a').first['href']
    str = ["\"#{category}\"","\"#{title}\"","\"#{item_code}\"","\"#{mrp_price}\"","\"#{dis_price}\"","\"#{description}\"","\"#{image}\""].join(",")
    output << str << "\n"
  end
  File.open("gofit-#{index}.csv","w"){|f|f.write output}
  puts "#{index} has completed"