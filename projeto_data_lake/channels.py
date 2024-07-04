import requests
import json

url = "https://www.googleapis.com/youtube/v3/channels?key=AIzaSyBsU4C5_AyS1GCP_K0Ji_ka1gKt0QizA1Q&part=statistics&id=UCR23kQs4jbLr-Kzjehwif8A"

response = requests.request("GET", url)

print(json.dumps(response.json(), indent=4, sort_keys=True)) 

with open("datalake\Bronze\channels.json", "w") as outfile:
    json.dump(response.json(), outfile)


