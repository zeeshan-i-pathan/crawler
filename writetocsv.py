import csv
# function to write array to csv file
def write_to_file(array,name):
  with open(name+".csv","wb") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for element in array:
      element = [s.replace("\n","").encode('utf-8') for s in element]
      spamwriter.writerow(element)
