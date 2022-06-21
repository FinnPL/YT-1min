#scrap youtube recommendation of a video
from threading import main_thread
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
import re
import json
import urllib
import config




def get_recommendation(video_url):
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    response = session.get(video_url)
    # execute Java-script
    response.html.render(sleep=2)
    # create bs object to parse HTML
    soup = bs(response.html.html, "html.parser")

    recom_ids = list()
    recom_ids.append('video_url')

    for a in soup.find_all('a', href=True):
        x = a['href']
        if re.search("/watch\?v=", x):
            x=x.replace("/watch?v=", "")
            if x not in recom_ids:
                recom_ids.append(x)
    
    recom_ids.remove('video_url')
    return recom_ids

def check_vidio_length(video_id):
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+config.api_key+"&part=contentDetails"
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    duration=contentDetails['duration']
    #print (duration)
    return duration

def is_shorter_than_1min(duration):
    if "M" not in duration and "H" not in duration:
        #print("true!!")
        return True



def main():
    list = get_recommendation('https://www.youtube.com/watch?v=xqFTe96OWPU')
    print(list)
    for i in list:
       if is_shorter_than_1min(check_vidio_length(i)):
           print("https://www.youtube.com/watch?v="+i)

       #if is_shorter_than_1min(x):
       #     print(i +" : " +x)



if __name__ == "__main__":
    main()