from __future__ import unicode_literals
#selenium imports
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
#youtube-dl and supporters imports
import os
#os.system("pip install -U -q -q -q yt-dlp") #this will install youtube dl if it isn't already
#os.system("pip install -U -q -q -q selenium") #the -q -q -q will supress any pip errors (path error)
#os.system("pip install -U -q -q -q audioread") 
from yt_dlp import YoutubeDL
import os
#generic imports
import time

"""
We doing that object oriented shit now (sad)
"""
class ytScraper:
    def __init__(self):
        ffox_options = Options() 
        ffox_options.add_argument("--headless") #this will make the browser headless (runs invisibly)
        ffox_options.add_argument("--log-level=3") #log level 3 supresses all output to the console
        serviceObject = Service("geckodriver.exe") #required selenium thing
        self.driver = webdriver.Chrome(service=serviceObject, options=ffox_options)
        
        #configure youtube-dl
        self.ydl_opts_video = {
            'format': 'mp4/bestaudio/best',
            'quiet': True,
            'sponsorblock': 'remove-sponsor/all',
            'cookiesfrombrowser': ('firefox',)  # Correct way
        }
        self.ydl_opts_audio = {
            'format': 'm4a/bestaudio/best',
            'quiet': True,
            'sponsorblock': 'remove-sponsor/all',
            'cookiesfrombrowser': ('firefox',)  # Correct way
        }
        
        print("Initialization Complete")
    def findAndPlay(self, songname):
        self.driver.get("https://www.youtube.com/results?search_query=" + songname)
        # Wait for the page to load and get results
        titles = []
        while not titles:
            print("DEBUG: Attempting to find song")
            time.sleep(0.5)
            titles = self.driver.find_elements(By.ID, 'video-title')
        # Get the first video URL
        first_url = titles[0].get_attribute('href')
        if not first_url:
            print("DEBUG: No valid video found")
            return
        URLS = [first_url]
        with YoutubeDL(self.ydl_opts_audio) as ydl:
            print("DEBUG: Downloading song")
            ydl.download(URLS)
            print(f"Found songs: {len(titles)}")
            outfile = ydl.prepare_filename(ydl.extract_info(URLS[0], download=False))
        os.rename(outfile, os.path.join("_temp", os.path.basename(outfile))) # move to _temp
        print("DEBUG: song downloaded to _temp folder")
        return
    
    def getMetadataList(self, query):
        self.driver.get("https://www.youtube.com/results?search_query=" + query)
        meta_list = []
        #accounting for slow loads
        while not meta_list:
            meta_list = self.driver.find_elements(By.ID, 'video-title')
            time.sleep(0.5)
        hrefs = [meta.get_attribute('href') for meta in meta_list]
        titles = [meta.get_attribute('title') for meta in meta_list]
        return hrefs, titles
        
    def getVideo(self, URL):
        print(f"running getVideo with URL {URL}")
        with YoutubeDL(self.ydl_opts_video) as ydl:
            if len(URL) == 1:
                ydl.download(URL)
            else:
                ydl.download(URL[0])
            outfile = ydl.prepare_filename(ydl.extract_info(URL, download=False))
        os.rename(outfile, os.path.join('web/temp/', os.path.basename(outfile)))
        return
            
        
            
        
        
                