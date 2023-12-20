import requests

url = 'http://localhost:2222/predict'

text = 'Message here'
response = requests.post(url, json=text).json()
print(); print(response)

if response['outcome'] == 1:
    print('Spam')
else:
    print('Not Spam')