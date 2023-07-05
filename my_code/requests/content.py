import os
import requests

# response = requests.get(url='https://jsonplaceholder.typicode.com/todos/')
# print(response.json()[:10])
# print(response.text)
# print(type(response.json()))
# print(type(response.text))

# response = requests.get(url='http://httbin.org/')
# print(response.text)

dir_name = os.getcwd()
file_name = 'image.jpeg'
file_path = os.path.join(dir_name, os.path.join('data', file_name))

with open(file_path, 'wb') as file:
    response = requests.get(url='http://httpbin.org/image/jpeg', timeout=30)
    file.write(response.content)
