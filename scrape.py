import time
import urllib.request
import json
from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

while True:
    source = urllib.request.urlopen('https://portal.rockgympro.com/portal/public/bc4d3be86f2f8564a4e5e4f9151f6bf6/occupancy?&iframeid=occupancyCounter&fId=1837').read()
    soup = BeautifulSoup(source,'html.parser')
    
    # find the person count in the json bit stored in the html
    # cleaning json is not intuitive...
    rawJ = soup.find_all('script')[2]
    J = str(rawJ)
    J1 = J.split("'CNP' : ") # this is the climb nittany data, they also had other gym
    J2 = J1[1].split(';')
    J3 = J2[0].replace("\n", "")
    J4 = J3.rsplit(',',1)
    J5 = J4[0].replace("'",'"') # not sure why their code uses '' instead of ""
    s = json.loads(J5)
    c = s["count"]
    
    # get the date and time
    now = datetime.now()
    ct = now.strftime("%D %H:%M:%S")
    wkd = now.weekday()
    # write the data to csv
    append_list_as_row('data.csv', [ct,wkd,c])
    
    print(str(c)+' people at gym on '+ct)
    # sleep for 10 minutes
    time.sleep(10*60)