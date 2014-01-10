require 'nokogiri'
require 'open-uri'
output = ""
newproduct = ""
puts "Opening Homepage"
homepage = Nokogiri.HTML(open("http://www.championsports.in/index.php"));1
links = []
homepage.css('#ja-sidenav li.level0').each do |link|
  link = link.css('a')
  text = link.css('span')
  if link.count > 1
    (1...link.count).each {|x| links << {:parent => text[0].text,:link => link[x]['href'],:child => text[x].text} }
  else
    links << {:parent => text.first.text,:link => link.first['href'], :child => ""}
  end
end

def openpage(link)
  page = Nokogiri.HTML(open(link[:link]+"?limit=30"));1
  products ||= []
  products << page.css('.products-grid li.item').collect {|x| x.css('a').first['href'] };1
  begin
  	nextpage = {:link => page.css('.pager ol li .next').last['href'], :parent => link[:parent], :child => link[:child] }
  	products << openpage(nextpage)
  rescue
  end
  products
end

file = File.open "championsport.csv"
visitedProducts=[]; CSV.parse(a) {|x| visitedProducts << x[-1]; output << x.to_s << "\n" }

links.each do |link|
  allproducts = openpage(link).flatten!
  allproducts.each do |product|
    unless visitedProducts.include? product
      puts "Adding product..."
      page = Nokogiri.HTML(open(product));1
      product_id = page.css('input[type="hidden"]').first['value']
      title = page.css('.product-name h1').text
      category = link[:parent] + " - " + link[:child]
      item_code = product_id
      dis_price = ""
      mrp_price = page.css('.regular-price .price').text.gsub('Rs','').gsub(',','')
      image = page.css('.product-image img').first['src']
      description =  page.css('.box-description').first.content.gsub("\"","")
      str = ["\"#{category}\"","\"#{title}\"","\"#{item_code}\"","\"#{mrp_price}\"","\"#{dis_price}\"","\"#{description}\"","\"#{image}\"","\"#{product}\""].join(",")
      output << str << "\n"
      newproduct << str << "\n"
    end
  end
end
File.open("championsport.csv","w"){|f|f.write output}
File.open("championsport-newproducts.csv","w"){|f|f.write newproduct}