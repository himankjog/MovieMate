from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import time

# For text to speech
from gtts import gTTS
import os

#For sentianal 
import tweepy
from textblob import TextBlob
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt; plt.rcdefaults()

# FOR Telegram
import telepot
# Functions

def camel(movie):
	title = ""
	for i in movie.split():
		title += i[0].upper() + i[1:]
	return title

#FOR Twitter and Telgram
def tweetel(movie):
	chat_id1 = '-177094990'
	file_id1 = 'http://mw2.google.com/mw-panoramio/photos/medium/88068769.jpg' 
	#file_id1 = '/home/aaditya/Desktop/img123.jpg' 
	bot=telepot.Bot('319826203:AAFtepbgGeh01st22GIFQAHk_gC8ZE8qpvE')                                                          
	bot.sendMessage(chat_id1,movie+ ' has really good reviews ! We should watch it.')
	#bot.sendPhoto(chat_id1,file_id1)

	#==================================================================

	CONSUMER_KEY ="tn2zlRaR9kqrPc10nAmlyRuWS"
	CONSUMER_SECRET = "ZCStbkI2JqgjEfIXoJlwU31IJ9TXjIpxPxT19mMmQlEdeMFWSD"   
	ACCESS_KEY = "853412742723710976-GnRdTjLyRQWAk2NwciA6HhDCuDNSCVD"    
	ACCESS_SECRET = "KHWCYDz5tIuTGfEuj4EHOq1EFYOKJufaf8TsFNVdN8Fmr"

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

	api = tweepy.API(auth)
	api.update_status('#'+camel(movie)+" is really awesome. I recommend it")




def sentinal(movie):
	consumer_key= 'uGwMIcH6IucreFS7PElKohpvd'
	consumer_secret= 'a3JWzjWnvCaICZXOZIZvKrtoXOEClflyOXHNruu9DZpcm88mTx'

	access_token='853958079985143808-PU3wBPKZ1GXEOsQhlKTmkD8Kt9kPoof'
	access_token_secret='LESLGtPC1nF4Ofa06Uh6KZ1eCMKEUXOxW6zApRBqWA9TT'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)



	inp = movie
	target = "".join(inp.split())
	public_tweets = api.search(target)
	#print(literal_eval(public_tweets))
	#public_tweets1 = public_tweets+'review' 


	csvfile = open('twitter_sentiment.csv', 'wb')
	writer = csv.writer(csvfile)   

	count_worst = 0 ;
	count_not_good = 0 ;
	count_worse = 0 ;
	count_neutral = 0 ;
	count_good = 0 ;
	count_very_good = 0 ;
	count_excel = 0 ;


	for tweet in public_tweets:
	    foo = tweet.text.encode('utf-8').strip()  

	    analysis = TextBlob(tweet.text).sentiment
	    emotion = analysis.polarity
	    if emotion >= -1 and emotion < -0.7 :
	       count_worst = count_worst +1
	       writer.writerow([foo,"worst",analysis])
	    elif emotion >=-0.7 and emotion < -0.5 :
	       count_worse = count_worse +1
	       writer.writerow([foo,"worse",analysis])
	    elif emotion > -0.5 and emotion < -0.3 :
	       count_not_good = count_not_good +1
	       writer.writerow([foo,"not good",analysis])
	    elif emotion > -0.3 and emotion < 0.1 :
	       count_neutral = count_neutral +1
	       writer.writerow([foo,"neutral",analysis])
	    elif emotion >= 0.1 and emotion < 0.5  :
	       count_good = count_good +1  
	       writer.writerow([foo,"good",analysis])
	    elif emotion >= 0.5 and emotion <= 0.7  :
	       count_very_good = count_very_good +1  
	       writer.writerow([foo,"very good",analysis])
	    else :
	       count_excel = count_excel +1  
	       writer.writerow([foo,"excellent",analysis])         
	    
	csvfile.close() 

	labels = 'worst', 'worse', 'Not good', 'Neutral', 'Good', 'Very good', 'Excellent !'
	ctr = 0
	if count_worst == 0:
	  count_worst = ctr+1
	  ctr += 1
	if count_worse == 0:
	  count_worse = ctr+1
	  ctr += 1
	if(count_not_good == 0):
	  count_not_good = ctr+1;
	  ctr -=1
	if(count_neutral == 0):
	  count_neutral = ctr+1
	  ctr += 1
	if(count_good == 0):
	  count_good = ctr+1
	  ctr -= 1
	if(count_very_good == 0):
	  count_very_good = ctr+1
	  ctr += 1
	if(count_excel == 0):
	  count_excel = ctr+1;
	sizes = [count_worst,count_worse,count_not_good,count_neutral ,count_good, count_very_good, count_excel]
	explode = (0,0,0,0,0,0,0)  
	patches, texts = plt.pie(sizes, shadow=True, startangle=90)
	plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
	#plt.legend(title="User reactions to the movie" + target)
	#plt.legend(patches, labels, loc="lower left")

	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	plt.show()

	time.sleep(1)
	plt.close('all')
	#############################


def imdb_rating(movie):
	movie = str(movie)
	link = requests.get("https://www.google.co.in/search?q="+movie+"+imdb")
	soup = BeautifulSoup(link.text,'html.parser')
	html = soup.find('h3',{'class' : 'r'})
	href = (html.a).get('href')
	href = href.split('&')
	# print "\n\n    href : ",href[0][7:]
	link = requests.get(href[0][7:])
	soup = BeautifulSoup(link.text,'html.parser')
	html = soup.find('strong')
	# print "\n\n    html : ",html
	title = html.get('title')
	print "\n\nIMDB Rating of ",movie," : ",title,"\n\n"
	print "Description\n"
	des = soup.find('div',{'class','summary_text'})
	print (des.text).lstrip(),"\n\n"
	language = 'en'
	mytext = (des.text).lstrip()
	myobj = gTTS(text=mytext, lang=language, slow=False)
 	myobj.save(movie.split()[0]+".mp3")
 	os.system("mpg321 "+movie.split()[0]+".mp3")

def decorate_name(movie):
	return "+".join(movie.split())

def movies():
	movie = raw_input("Input movie name you wish to download\t:\t")
	movie_name = decorate_name(movie)
	imdb_rating(movie)
	print "Now some analysis on the basis of Tweets :"
	sentinal(movie)
	choice = raw_input("Do you still wish to download?\nPress y for yes, Press n for no\t:\t")
	if choice == 'n': 
		print "Thank You"
	else:
		driver = webdriver.Firefox()
		print "\nOpening search page\n"

		driver.get("https://www.google.co.in/search?q="+movie_name+"+movie+parent+directory")
		element = driver.find_elements_by_xpath("//h3[@class='r']")
		a=[]
		ct = 0
		for i in element:
			ct += 1
			a.append(i.find_element_by_xpath('a'))
			if ct == 10:
				break
		href=[]
		for i in a:
			href.append(i.get_attribute('href'))
		for h in href:	
			ctr = 0
			driver.get(h)
			for link in driver.find_elements_by_xpath('//a'):
				if(movie.split()[0].lower() in (link.get_attribute('href')).lower()):
					link.click()
					ctr = 1
					break
			if ctr == 1:
				break
	choice = raw_input("Do you wish to tell your friends about it too?\nPress y for yes, n for no\t:\t")
	if(choice == 'y'):
		tweetel(movie)
	print 'thank you'

def seasons():
	print 'Input season name you wish to download\t:\t' 
	print 'Make sure the first letter is an uppercase letter!!' 
	movie = raw_input()
	print 'Which season do u want to download' 
	season= int(input())
	print 'Starting from which episode' 
	epi_start= int(input())
	print 'To which episode' 
	epi_end=int(input())
	driver = webdriver.Firefox()
	actionChains = ActionChains(driver)
	for i in range(epi_start,epi_end):
		if i<10 :
			url="http://o2tvseries.com/"+movie+"/Season-0"+str(season)+"/Episode-0"+str(i)+"/index.html"
		else:
			url="http://o2tvseries.com/"+movie+"/Season-0"+str(season)+"/Episode-"+str(i)+"/index.html"
		message= "the program is downloading an episode"
		print message
		driver.get(url)
		textlink=movie+" - "+"S0"+str(season)+"E0"+str(i)+" (O2TvSeries.Com).mp4"
		linkElem = driver.find_element_by_link_text(textlink)
		linkElem.click()
	driver.close()
	print 'thank you'

print "Press 1 to download movie\n 2 to download seasons\n"
choice = input()
if(choice == 1):
	movies()
else:
	seasons()



# print "\nOpened search page, Now opening movie page\n"
# element = driver.find_element_by_xpath("//a[@class='poster']")
# link = element.get_attribute('href')

# driver.get(link)
# print "\nOpened movie page, and writing to file\n"
# soup = BeautifulSoup(driver.page_source,'html.parser')
# f = open("raw",'w')
# f.write(soup.prettify().encode('UTF-8'))
# f.close()
# print "\n written to file, now clicking on the div\n"
# # element = driver.find_element_by_xpath("//div[@class='item mbtn download movie pull-right hidden']")
# element = driver.find_element_by_xpath("//div[@class='cover']")
# actionChains = ActionChains(driver)
# actionChains.click(element).perform()
# print "\n\n      URL of the PAGE",driver.current_url
# print "\n\n Click on Download Link\n"
# element = driver.find_element_by_xpath("//div[@class='item mbtn download movie pull-right hidden']")
# actionChains = ActionChains(driver)
# actionChains.click(element).perform()
# print "\n\n Downloading started\n"
# f = open("raw",'w')
# f.write(soup.prettify().encode('UTF-8'))
# f.close()
# https://fmovies.se/film/inception.zlzm/6yyxpz