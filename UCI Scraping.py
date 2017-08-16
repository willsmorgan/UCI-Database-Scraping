# Scraping practice - University of California, Irvine Machine Learning Responsitory
    #http://archive.ics.uci.edu/ml/datasets.html
    
"""
Created on Sun Aug  6 16:11:43 2017

@author: wsmorgan
"""
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import re
import pandas as pd 
import os as os#create directories if we need to


#Main file path
rootpath = r'C:\Users\wsmorgan\Desktop\Random Data\UCI Machine Learning Repository/'

#The code below reassigns the default download folder for the Chrome browser so we can isolate the files for every given year. 
chromeOptions = webdriver.ChromeOptions()
#Make sure to update the path depending on the computer you're working on. 
prefs = {"download.default_directory" : rootpath}
chromeOptions.add_experimental_option("prefs", prefs)
#Here we are opening the browser and designating the web driver with the new default download folder. 
driver = webdriver.Chrome(chrome_options=chromeOptions)
#Tell the driver to wait 30 seconds before proceeding with the next action, if nothing has happened. 
driver.implicitly_wait(30)


#Base URL
base_url = 'http://archive.ics.uci.edu/ml/'
driver.get(base_url + 'datasets.html')

#Grab the source information for the current page
soup = BeautifulSoup(driver.page_source)

#From the current soup object, identify the table that contains the table of links that we want
table = soup.findAll('table', border = '1', cellpadding = '5')
rows = table[0].findAll('tr')

del rows[0] #first row is the names of the columns
rows = rows[::2] #the even indexed rows contains enough information

links = []
ds_name = []
ds_type = []
ds_task = []
ds_numobs = []
ds_numvars = []

for row in rows:  
    #Grab information about the data set and store it separately
    items = row.findAll('p', 'normal')    
    ds_name.append(items[0].get_text())
    ds_type.append(items[1].get_text())
    ds_task.append(items[2].get_text())
    ds_numobs.append(items[4].get_text())
    ds_numvars.append(items[5].get_text())

    #Grab links to invdividual data sets
    for link in row.findAll('a'):
        links.append(link.get('href'))

#Minor cleaning before we continue
links = links[::2]
ds_info = [ds_name, ds_numobs, ds_numvars, ds_task, ds_task]
for ds in ds_info:
   ds = [d.replace("\xa0", "") for d in ds]

ds_name = None
ds_numobs = None
ds_numvars = None
ds_task = None
ds_type = None

#Throw data set information into a DF so it can be saved for reference later
ds_info = pd.DataFrame({"ds_name" : ds_info[0],
                   "numobs" : ds_info[1],
                    "numvars" : ds_info[2],
                    "task" : ds_info[3],
                    "type" : ds_info[4]})
    
#we need to keep track of the index in order to grab the correct data set names
i = 0

for link in links:
    
    #grab the name of the data set you are trying to find
    name = ds_info.iloc[i, 0]
    
    #go to the main page of the data set
    temp_base = base_url + link + "/"
    driver.get(temp_base)
    soup2 = BeautifulSoup(driver.page_source)
    table = soup2.find('p')
    
    #find the link to the download page
    ds_link = table.find('a')
    ds_link = ds_link.get('href')[3:] + "/"
    
    #go to download page
    driver.get(base_url + ds_link)
    soup3 = BeautifulSoup(driver.page_source)
    
    dt_links = []
    for dt_link in soup3.findAll('a'):
        dt_links.append(dt_link.get('href'))    
    
    for dt_link in dt_links:
                
       
        #Create folder for dataset if it doesn't already exist
        folder = rootpath + name
        if not os.path.exists(rootpath + name):
            os.makedirs(folder)
        
        #Search for the data set
        if '.data' in dt_link:
            if '.data.Z' in dt_link or '.data.gz' in dt_link:
                driver.get(base_url + ds_link + dt_link)
            else:
                driver.get(base_url + ds_link + dt_link)
                data = BeautifulSoup(driver.page_source)
                data = data.find('pre')
                d_string = data.get_text()
                d_list = d_string.split()
                d_list = [ds.split(",") for ds in d_list]
                df = pd.DataFrame(d_list)
                fname = dt_link.replace('.data', '')
    
                #Save the pulled dataset into the new folder
                df.to_csv(folder + "\\" + name + "_data.csv", header = False)
        
        #Search for a README file
        elif '.names' in dt_link or ('.info' in dt_link and 'old' not in dt_link):
            driver.get(base_url + ds_link + dt_link)
            data = BeautifulSoup(driver.page_source)
            if os.path.isfile(folder + "\README.txt") == True:
                with open(folder + "\README.txt", 'w') as f:
                    for line in data.prettify():
                        f.write(str(line))
            else: 
                with open(folder + "\README.txt", 'x') as f:
                    for line in data.prettify():
                        f.write(str(line))
       
        
#        #Clean up the loop for the next iteration
#        unwanted = [d_string, d_list, df]
#        for obj in dir():
#            if obj in unwanted:
#                del obj
        
    i += 1
    
    
    
### CURRENT PROGRESS
 
### WHEN YOU COME BACK

### Specific Tasks
