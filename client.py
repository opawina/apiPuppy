import requests
import json
import time


start = time.time()

r = requests.get('http://localhost:33221')
print(r.status_code)
print(r.headers)
print(r.content)
data = json.loads(r.content.decode())
print(json.dumps(data, indent=2))

print(time.time() - start)
a=1

