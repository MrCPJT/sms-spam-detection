import requests

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

data = {'url': 'Hello World!'}

result = requests.post(url, json=data).json()
print(f'\nSpam? {result}')

print('===============')

if result == 0:
    print("Not Spam")
else:
    print("Spam")