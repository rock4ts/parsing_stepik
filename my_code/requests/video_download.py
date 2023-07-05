import os
import requests

url = 'https://parsinger.ru/video_downloads/videoplayback.mp4'

with open('../data/video.mp4', 'wb') as video:
    response = requests.get(url, stream=True)
    for piece in response.iter_content(chunk_size=10000):
        video.write(piece)

print(os.path.getsize('../data/video.mp4'))
