require 'nokogiri'
require 'open-uri'
require 'shellwords'
puts "Opening homepage"
homepage = Nokogiri.HTML(open("http://www.gofitindia.com/"));1
links = (homepage.css('ul#vmenu li a') - homepage.css('ul#vmenu li ul a'))
links = links.collect{|link| "http://www.gofitindia.com/"+link['href'] }
puts "Going through each link in the categories"
puts "Found #{links.size} links"
links.each_with_index do |link,index|
  puts "sending #{link} #{index}"
  `ruby getCategory.rb #{link.shellescape} #{index} &`
end