import requests
from bs4 import BeautifulSoup
from datetime import datetime
import binascii, re

def asciirepl(match):
  # replace the hexadecimal characters with ascii characters
  s = match.group()  
  return binascii.unhexlify(s)  

def reformat_content(data):
  p = re.compile(r'\\x(\w{2})')
  return p.sub(asciirepl, data)






pageStructure = ""

page = requests.get("http://indianexpress.com/section/sports/")
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

articlesData = []
totalPages = soup.find_all("a", { "class" : "page-numbers" })
print totalPages
totalPages = totalPages[-2].getText()
totalPages = totalPages.replace(",","")
print totalPages

for pageNumber in range(1355,int(totalPages)):

	page = requests.get("http://indianexpress.com/section/sports/page/" + str(pageNumber) + "/")
	print "http://indianexpress.com/section/sports/page/" + str(pageNumber) + "/"
	soup = BeautifulSoup(page.content, 'html.parser')


	articleList = soup.find_all("div", { "class" : "articles" })
	firstArticle = soup.find_all("div", { "class" : "articles first" })
	articleList.extend(firstArticle)
	for index in range(len(articleList)):
		try:
			date = articleList[index].find("div", { "class" : "date" })
			title = articleList[index].find("div", { "class" : "title" })
			snaps = articleList[index].find("div", { "class" : "snaps" })
			shortInfo = articleList[index].find('p')
			snapUrl = snaps.find('a')['href']
			snapUrl = snapUrl.split("/")
			sportCategory = snapUrl[5]
			imageSlot = snaps.find('a')
			imageSource = imageSlot.find('img')['data-lazy-src']
			alternateImageText = imageSlot.find('img')['alt']
			link = title.find('a')['href']
			linkDetails = requests.get(link)
			insideSoup = BeautifulSoup(linkDetails.content, 'html.parser')	
			article = insideSoup.find("div", { "class" : "articles" })
			fullDetails = article.find("div", { "class" : "full-details" })
			content = fullDetails.find_all('p')
			combinedText = ""
			for index in content:
				combinedText = combinedText + index.getText(strip=True) + "\n"
			imageCaption = fullDetails.find("span", { "class" : "custom-caption" })
			imageCaption = imageCaption.getText(strip=True)
			dateTimeArticle = datetime.strptime(date.getText(strip=True), '%B %d, %Y %I:%M %p')	
			currentArticleData = {
			"date" :  date.getText(strip=True),
			"title" : title.getText(strip=True).strip().replace(u'\xa0', u' '),
			"link" :  link,
			"shortInfo" : shortInfo.getText(strip=True).strip().replace(u'\xa0', u' '),
			"imageSource" :  imageSource,
			"alternateImageText" :  alternateImageText.replace(u'\xa0', u' '),
			"sport" : sportCategory,
			"info" : combinedText.replace(u'\xa0', u' '),
			"imageCaption" : imageCaption.replace(u'\xa0', u' '),
			"source" : "www.indianexpress.com"
			}
			print str(pageNumber)
			print currentArticleData
			print "\n\n\n\n"
		except:
			print "Unable to scrape : " + str(pageNumber)
