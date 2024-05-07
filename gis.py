import requests
import settings

def determineCoordinates(adress):
    # Ф-я для определения координат точки
    resp_url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={adress}&fields=items.point&key={settings.key}"
    response = requests.get(resp_url)
    lon = response.json()["result"]["items"][0]["point"]["lon"]
    lat = response.json()["result"]["items"][0]["point"]["lat"]
    return [lat, lon]
def PublicTransport(url, start, end):
    
    start_lat, start_lon = determineCoordinates(start)
    end_lat, end_lon = determineCoordinates(end)
    d = {
        "locale": "ru",
        "source":
        {
            "name": start,
            "point":
            {
                "lat": start_lat,
                "lon": start_lon
            }
        },
        "target":
        {
            "name": end,
            "point":
            {
                "lat": end_lat,
                "lon": end_lon
            }
        },
        "transport": ["bus", "tram"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=d, headers=headers)
    return resp.json()
