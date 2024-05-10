import requests
import settings
import time
import logging

logging.basicConfig(level=logging.INFO)


def determineCoordinates(address, index_token=0):
    try:
        resp_url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={address}&" \
                   f"fields=items.point&key={settings.keys[index_token]}"
        response = requests.get(resp_url)
        lat = response.json()["result"]["items"][0]["point"]["lat"]
        lon = response.json()["result"]["items"][0]["point"]["lon"]
        id = response.json()["result"]["items"][0]["id"]
    except Exception as exception:
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)
        return determineCoordinates(address, index_token+1)
    return [lat, lon, id]


def getLink(attrs, *args):
    try:
        points = [args[0]] + attrs
        return getRoute([determineCoordinates(point) for point in points])
    except Exception as e:
        logging.error(e)
        logging.error("2Gis ключ устарел")
        return False


def getSight(address, index_token=0):
    x, y, ind = determineCoordinates(address, index_token)
    url = settings.getSights + f"q=Достопримечательность&sort_point={y},{x}&key={settings.keys[index_token]}"
    try:
        response = requests.get(url)
        mas = response.json()["result"]["items"][0:10]
        arr = []
        for val in mas:
            arr.append(val["full_name"])
        return arr
    except requests.exceptions.InvalidSchema:
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)
        return getSight(address, index_token+1)


def getRoute(args, way="multimodal"):
    url = f"https://2gis.ru/directions/points/"
    for val in args:
        url += f"{val[1]}%2C{val[0]}%3B{val[2]}" + "%7C"
    return url


def makeRoute(args, index_token=0):
    status = 'Run'
    start =0
    try:
        agents = [{"agent_id": 0, "start_waypoint_id": 0, "finish_waypoint_id": len(args) - 1}]
        waypoints = []
        for i in range(len(args)):
            coordinates = determineCoordinates(args[i], index_token)
            waypoints.append({"waypoint_id": i, "point": {"lat": coordinates[0], "lon": coordinates[1]}})
        task_id = requests.post(settings.makeOpt + f"{settings.keys[index_token]}",
                    json={"agents": agents, "waypoints": waypoints}).json()["task_id"]
        time.sleep(2.5)
        response = requests.get(settings.getRoute + f"{task_id}&key={settings.keys[index_token]}").json()

        while status not in ['Done','Fail']:
            response = requests.get(settings.getRoute + f"{task_id}&key={settings.keys[index_token]}").json()
            status = response['status']
            logging.info(response['status'])
            if start > 0:
                time.sleep(2)
            start += 2
            logging.info(start)
            if start > 10:
                break
        logging.info(response)
        response = response["urls"]["url_vrp_solution"]

        mas = []
        for val in requests.get(response).json()["routes"][0]["points"]:
            mas.append(args[val])
        return mas
    except KeyError:
        logging.warning("Закончился ключ " + settings.keys[index_token])
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)

        makeRoute(args, index_token+1)
    except Exception as e:
        logging.error(e)
        logging.error("Закончились все ключи !!!")


def split(end, ans=""):
    if len(ans) == 0:
        return [end]
    l = ans.split("$")
    for i in range(len(l)):
        l[i] = f"{end}, {l[i]}"
    l.append(end)
    return l