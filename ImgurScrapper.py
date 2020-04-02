from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
import urllib.request
import requests
import uuid
import os

print("This script will take your search query and find the best images within the last week!")
search = input("Provide a search to query\n")
folder = input("What's the folder path we should save the file to?\n")
count = input("How many videos/images should we save?\n")
count = int(count)

imgurBaseUrl = 'https://imgur.com'
imgurSearchQuery = '/search/score/week?q='

browser =  webdriver.Chrome(executable_path='chrome_executable_path')

# Iterate through all gallery links and get the image/video. Download them individually.
def parseAndDownloadContent(link):
    #Download the image or video from the link. Parse and download.
    browser.implicitly_wait(3)
    browser.get(link)
    browser.find_elements_by_class_name('post-image-container')
    pageSource = browser.page_source
    soup = BeautifulSoup(pageSource, 'lxml')

    # Find all pictures 
    imgPlaceholders = soup.find_all('img', class_='image-placeholder')
    postImgPlaceholders = soup.find_all('img', class_='post-image-placeholder')
    pictureList = []

    for postImgPlaceholder in postImgPlaceholders:
        source = postImgPlaceholder['src']
        if 'https:' not in source:
            source = 'https:' + source
        pictureList.append(source)

    for imgPlaceholder in imgPlaceholders:
        source = imgPlaceholder['src']
        if 'https:' not in source:
            source = 'https:' + source
        pictureList.append(source)

    # Iterate and append random UUIDs to the downloaded images 
    for pictureLink in pictureList:
        urllib.request.urlretrieve(pictureLink, folder + '\\' + str(uuid.uuid4()) + '.jpg') 

    # Find all videos 
    videos = soup.find_all('video')
    videoList = []
    for video in videos:
        sourceObj = video.find('source')
        if sourceObj == None:
            break
        else:   
            source = sourceObj['src']
        if 'https:' not in source:
            source = 'https:' + source
        videoList.append(source)

    for link in videoList:
        urllib.request.urlretrieve(link, folder + '\\' + str(uuid.uuid4()) + '.mp4') 
    return True

response = requests.get(imgurBaseUrl + imgurSearchQuery + search)
soup = BeautifulSoup(response.text, 'lxml')
imageLists = soup.find_all('a', class_='image-list-link')

imageLinks = []
for img in imageLists:
    link = img.get('href')
    imageLinks.append(imgurBaseUrl + link)

if os.path.isdir(folder) == True:
    downloadedCount = 0
    for link in imageLinks:
        if parseAndDownloadContent(link) == True:
            downloadedCount = downloadedCount + 1
            if(downloadedCount >= count): 
                browser.close()
                break
else:
    print("Folder is not a directory")

