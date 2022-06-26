from operator import contains
from urllib import request, response
from googleapiclient.discovery import build
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
import config
import time
import re
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

api_key = config.api_key

youtube = build('youtube', 'v3', developerKey=api_key)


#Get youtube video length
def get_video_length(video_id):
    request  = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    response = request.execute()
    return response['items'][0]['contentDetails']['duration']

def is_shorter_than_1min(video_id):
    x = get_video_length(video_id)
    if "M" not in x and "H" not in x and "S" in x:
        return True
    return False

def get_recommendation(video_url):
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    print ("Searching in " +video_url)
    response = session.get(video_url)
    # execute Java-script
    response.html.render(sleep=2)
    time.sleep(2)
    # create bs object to parse HTML
    soup = bs(response.html.html, "html.parser")

    recom_ids = list()
    recom_ids.append('video_url')

    for a in soup.find_all('a', href=True):
        x = a['href']
        if re.search("/watch\?v=", x):
            x=x.replace("/watch?v=", "")
            x=x.replace('https://www.youtube.com','')
            if x not in recom_ids and "&pp=" not in x and "&t=" not in x and "&list=" not in x:
                recom_ids.append(x)

    recom_ids.remove('video_url')
    return recom_ids


def rabit(video_url,found_list):
    if (found_list.__len__()>=50):
        return found_list

    list = get_recommendation(video_url)
    print ('Liste: ')
    print (list)
    if not list:
        print("keine Liste")
        return;
    for i in list:
        if is_shorter_than_1min(i):
            if i not in found_list:
                print("Video gefunden: " + i)
                found_list.append(i)
                return_list= rabit("https://www.youtube.com/watch?v="+i,found_list)
                if return_list:
                    return return_list




found_list = list()
list2 = list()
list2 = rabit("https://www.youtube.com/watch?v=hdWFXa_KqN0",found_list)
for i in list2:
    print("https://www.youtube.com/watch?v="+i)