import requests

URL = 'https://maytinhvui.com/wp-content/uploads/2020/11/hinh-nen-may-tinh-4k-game-min.jpg'
response = requests.get(URL,  stream=True)
print("TEST")