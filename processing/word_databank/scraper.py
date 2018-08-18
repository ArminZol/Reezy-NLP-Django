from bs4 import BeautifulSoup
import urlparse, urllib
from saver import save

start_url = 'https://www.thestar.com/'
url_check = start_url

urls = [start_url]
visited = []

FILE_NAME = 'text.txt'

stop = False

while len(urls) > 0:
	text = []
	
	try:
		html_text = urllib.urlopen(urls[0]).read()
	except:
		print 'Error on:', urls[0]

	soup = BeautifulSoup(html_text)

	print 'URL:', urls[0]
	urls.pop(0)
	print 'Url Count:', len(urls)

	for tag in soup.findAll('p'):
		if tag.string != None:
			text.append(tag.string)

	for tag in soup.findAll('a', href=True):
		tag['href'] = urlparse.urljoin(start_url, tag['href'])
		print 'Tag:', tag['href']

		if url_check in tag['href'] and tag['href'] not in visited and not stop:
			urls.append(tag['href'])
			visited.append(tag['href'])

			if len(urls) >= 5000:
				stop = True

	save(text, FILE_NAME)

print '---------------------'