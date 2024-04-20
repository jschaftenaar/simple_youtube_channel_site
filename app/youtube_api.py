from googleapiclient.discovery import build
import os
from diskcache import Cache

cache = Cache('./cache')

def youtube_client():
    return build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

@cache.memoize(expire=3600)
def get_channel_videos(channel_id):
    youtube = youtube_client()
    # Fetch all videos and playlists from the channel
    videos = []
    next_page_token = None

    while True:
        res = youtube.search().list(
            channelId=channel_id, part="snippet", type="video",
            maxResults=50, pageToken=next_page_token
        ).execute()

        videos.extend(res['items'])
        next_page_token = res.get('nextPageToken')

        if not next_page_token:
            break

    return videos

@cache.memoize(expire=3600) 
def get_channel_playlists(channel_id):
    youtube = youtube_client()
    playlists = []
    next_page_token = None

    while True:
        res = youtube.playlists().list(
            channelId=channel_id, part="snippet",
            maxResults=20, pageToken=next_page_token
        ).execute()

        playlists.extend(res['items'])
        next_page_token = res.get('nextPageToken')

        if not next_page_token:
            break

    return playlists

@cache.memoize(expire=3600) 
def get_channel_info(channel_id):
    youtube = youtube_client()
    res = youtube.channels().list(
        id=channel_id, part="snippet,contentDetails,brandingSettings"
    ).execute()
    if 'items' in res and len(res['items']):
        return res['items'][0]
    return None

@cache.memoize(expire=3600) 
def get_video_details(video_id):
    youtube = youtube_client()
    video_response = youtube.videos().list(
        id=video_id,
        part="snippet,contentDetails,player"
    ).execute()

    if video_response['items']:
        return video_response['items'][0]
    return None
