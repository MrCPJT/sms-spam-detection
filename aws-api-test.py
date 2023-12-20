import requests

url = 'https://rw3gt8vdd5.execute-api.eu-west-2.amazonaws.com/Test/predict'

data = {'url': 'Hello World!'}

result = requests.post(url, json=data).json()
print(f'\nSpam? {result}')

print('===============')

if result == 0:
    print("Not Spam")
else:
    print("Spam")