#scrap youtube recommendation of a video
from http.client import FOUND
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
    print (video_url)
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
            x=x.replace('https://www.youtube.com','')
            if x not in recom_ids:
                recom_ids.append(x)
    
    recom_ids.remove('video_url')
    return recom_ids

def check_vidio_length(video_id):
    #video_id =video_id.replace('https://www.youtube.com','')
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+config.api_key+"&part=contentDetails"
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    duration=contentDetails['duration']
    return duration

def is_shorter_than_1min(duration):
    if "M" not in duration and "H" not in duration:
        return True



def get_next_20(seed_video_url,index,list):
    if index<=20:
        found=False
        list = get_recommendation(seed_video_url)
        while not found:
            if not list:
                list = get_recommendation(seed_video_url)
            for i in list:
                if is_shorter_than_1min(check_vidio_length(i)):
                    found = True
                    list2 =get_next_20("https://www.youtube.com/watch?v="+i,index+1,list)
                    return list2;
    else:
        return;

def main():
    result = list() 
    recom_ids = list()
    result =get_next_20("https://www.youtube.com/watch?v=xqFTe96OWPU",0,recom_ids)
    print (result)
    
    #list = get_recommendation('https://www.youtube.com/watch?v=xqFTe96OWPU')
    #print(list)
    #for i in list:
    #   if is_shorter_than_1min(check_vidio_length(i)):
    #       print("https://www.youtube.com/watch?v="+i)



if __name__ == "__main__":
    main()