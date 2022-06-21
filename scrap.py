#scrap youtube recommendation of a video
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs


video_url = "https://www.youtube.com/watch?v=xqFTe96OWPU"

# init an HTML Session
session = HTMLSession()
# get the html content
response = session.get(video_url)
# execute Java-script
response.html.render(sleep=1)
# create bs object to parse HTML
soup = bs(response.html.html, "html.parser")

print (soup.find_all("meta"))