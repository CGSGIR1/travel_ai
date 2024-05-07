import requests
import settings

def determineCoordinates(adress):
    # Ф-я для определения координат точки
    resp_url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={adress}&fields=items.point&key={settings.token}"
    response = requests.get(resp_url)
    lat = response.json()["result"]["items"][0]["point"]["lat"]
    lon = response.json()["result"]["items"][0]["point"]["lon"]
    id = response.json()["result"]["items"][0]["id"]
    return [lat, lon, id]
def getLink(*args):
    return getRoute([determineCoordinates(val) for val in args])
def PublicTransport(url, start, end):
    start_lat, start_lon = determineCoordinates(start)[:2]
    end_lat, end_lon = determineCoordinates(end)[:2]
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

def DirectionsAPI(url, start, end, trans_type):
    start_lat, start_lon = determineCoordinates(start)[:2]
    end_lat, end_lon = determineCoordinates(end)[:2]

def getSight(x, y):
    url = settings.getSights + f"q=Достопримечательность&sort_point={x},{y}&key={settings.token}"
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.InvalidSchema:
        return {"status": "400"}


def getRoute(args, way="multimodal"):
    url = f"https://2gis.ru/directions/points/"
    for val in args:
        url += f"{val[1]}%2C{val[0]}%3B{val[2]}" + "%7C"
    return url