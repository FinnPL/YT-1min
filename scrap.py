import time
import re
from urllib import request, response
from googleapiclient.discovery import build
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import config

api_key = config.api_key

youtube = build('youtube', 'v3', developerKey=api_key)


# Get youtube video length
def get_video_length(video_id):
    """
    Get the length of a youtube video.

    Parameters
    ----------
    video_id : String
        The youtube video id.

    Returns
    -------
    String
        The length of the video as PT#M#S.
    """
    request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    response = request.execute()
    return response['items'][0]['contentDetails']['duration']


def is_shorter_than_1min(video_id):
    """
    Check if a youtube video is shorter than 1 minute.

    Parameters
    ----------
    video_id : String
        The youtube video id.

    Returns
    -------
    Boolean
        True if the video is shorter than 1 minute.
    """
    length = get_video_length(video_id)
    if "M" not in length and "H" not in length and "S" in length :
        return True
    return False


def get_recommendation(video_url):
    """
    Get the recommendations for a youtube video.

    Parameters
    ----------
    video_url : String
        The youtube video url.

    Returns
    -------
    List
        The recommendations for the video (Video IDs).
    """
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    print("Searching in " + video_url)
    response = session.get(video_url)
    # execute Java-script
    response.html.render(sleep=2)
    time.sleep(2)
    # create bs object to parse HTML
    soup = bs(response.html.html, "html.parser")

    recom_ids = ['video_url']

    for tag in soup.find_all('a', href=True):
        link = tag['href']
        if re.search(r"/watch\?v=", link):
            link = link.replace("/watch?v=", "")
            link = link.replace('https://www.youtube.com', '')
            if link not in recom_ids and "&pp=" not in link and "&t=" not in link and "&list=" not in link:
                recom_ids.append(link)

    recom_ids.remove('video_url')
    return recom_ids


def rabit(video_url, found_list):
    """
    Get the recommendations for a youtube video.

    Parameters
    ----------
    video_url : String
        The youtube video url.
    found_list : List
        The list of already found Vidoes.

    Returns
    -------
    List
        The found videos (Video IDs).
    """
    if found_list.__len__() >= 50:
        return found_list

    list = get_recommendation(video_url)
    print('Liste: ')
    print(list)
    if not list:
        print("keine Liste")
        return
    for i in list:
        if is_shorter_than_1min(i) and i not in found_list:
            print("Video gefunden: " + i)
            found_list.append(i)
            return_list = rabit(
                    "https://www.youtube.com/watch?v="+i, found_list)
            if return_list:
                return return_list

def main():
    """MAIN TEST FUNCTION"""
    found_list = []
    list2 = []
    list2 = rabit("https://www.youtube.com/watch?v=hdWFXa_KqN0", found_list)
    for i in list2:
        print("https://www.youtube.com/watch?v="+i)


if __name__ == "__main__":
    main()
