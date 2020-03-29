from bs4 import BeautifulSoup
import requests

# Iterate through all gallery links and get the image/video. Download them individually.
def parseAndDownloadContent(link):
    #Download the image or video from the link. Parse and download. 
    print(link)

def validateFolder(folder):
    #Makes sure the folder is acccessible and can be accessed 
    print(folder)


print("This script will take your search query and find the best images within the last week!")
search = input("Provide a search to query\n")
folder = input("What's the folder path we should save the file to?\n")

imgurBaseUrl = 'https://imgur.com'
imgurSearchQuery = '/search/score/week?q='

response = requests.get(imgurBaseUrl + imgurSearchQuery + search)
soup = BeautifulSoup(response.text, 'lxml')
imageLists = soup.find_all('a', class_='image-list-link')

imageLinks = []
for img in imageLists:
    link = img.get('href')
    imageLinks.append(imgurBaseUrl + link)

validateFolder(folder)

for link in imageLinks:
    parseAndDownloadContent(link)

