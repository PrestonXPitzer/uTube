import eel
from ytcli import ytScraper
import os

yt = ytScraper()

eel.init("web")

@eel.expose
def search_backend(query):
    print(f'Searching youtube for {query}')
    video_links, strings = yt.getMetadataList(query=query)
    results = [{"name": s, "video": v} for s, v in zip(strings, video_links)]
    return results
    
@eel.expose
def get_video(URL):
    print(f'get_video called with URL: {URL}')
    yt.getVideo(URL)
    #send the JS function the url
    temp_paths = os.listdir('web/temp')
    print(temp_paths[0])
    return temp_paths[0]

try:
    eel.start("index.html", size=(800, 600))
except(SystemExit, KeyboardInterrupt):
    for f in os.listdir('web/temp'):
        os.remove(f'web/temp/{f}')


