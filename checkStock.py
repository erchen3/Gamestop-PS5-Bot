
import urllib.request
from bs4 import BeautifulSoup
import json
import smtplib, ssl
from getpass import getpass
import time


URL = "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html?utm_source=rakutenls&utm_medium=affiliate&utm_content=GameSpot&utm_campaign=10&utm_kxconfid=tebx5rmj3&cid=afl_10000087&affID=77777&sourceID=VZfI20jEa0c-WzwrXqb7Wb_hPipbQaatmw"
port = 465 #SSL port.
sender_email = ""
receiver_email = ""

def main():
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		#Step 0: log in
		server.login(sender_email,getpass())

		while True:

			#Step 1: Get the http response of interest and then feed it to beautifulsoup to begin processing.
			request = urllib.request.Request(
				URL,
				data = None,
				headers = {
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
				}
			)

			response = urllib.request.urlopen(request)
			soup = BeautifulSoup(response.read(), 'html.parser')
			#Step 2: Begin DOM manipulation.
			metaData = soup.find("button", {"class":"add-to-cart btn btn-primary"})['data-gtmdata']

			convertedData = json.loads(metaData)
			
			#Step 3: Check availability.
			if convertedData['productInfo']['availability'] != 'Not Available':
				server.sendmail(sender_email, receiver_email, "PS5 is Available!")
				time.sleep(2)
			else:
				time.sleep(60)

if __name__ == "__main__":
	main()
