import json
import requests

# lon = float(input())
# lat = float(input())
url = "https://routing.api.2gis.com/public_transport/2.0?key=d6eac903-d3d2-45f0-8345-981f03a9c39a"
resp = requests.get(url)
print(resp)