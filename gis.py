import requests
import settings


def PublicTransport(url):
    d = {
        "locale": "ru",
        "source":
            {
                "name": "Point A",
                "point":
                    {
                        "lat": 51.734588,
                        "lon": 36.149328
                    }
            },
        "target":
            {
                "name": "Point B",
                "point":
                    {
                        "lat": 51.734183,
                        "lon": 36.176865
                    }
            },
        "transport": ["bus", "tram"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=d, headers=headers)
    return resp


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
        url += f"{val[0]}%2C{val[1]}%3B{val[2]}" + "%7C"
    return url
