import os

import requests

base_url = 'https://parsinger.ru/img_download/img/ready/'
image_dir_name = 'images'
image_dir = os.path.join(os.getcwd(), os.path.join('data', image_dir_name))

if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

for i in range(1, 161):
    image_path = os.path.join(image_dir, f"{i}.png")
    with open(image_path, 'wb') as image_file:
        image_url = f"{base_url}{i}.png"
        response = requests.get(image_url, timeout=15)
        image_file.write(response.content)
