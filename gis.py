import requests
import settings
import time
import logging

logging.basicConfig(level=logging.INFO)
index_token = 0


def determineCoordinates(address):
    global index_token
    try:
        resp_url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={address}&" \
                   f"fields=items.point&key={settings.keys[index_token]}"
        response = requests.get(resp_url)
        lat = response.json()["result"]["items"][0]["point"]["lat"]
        lon = response.json()["result"]["items"][0]["point"]["lon"]
        id = response.json()["result"]["items"][0]["id"]
    except Exception as exception:
        index_token += 1
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)
        return determineCoordinates(address)
    return [lat, lon, id]


def getLink(*args):
    try:
        return getRoute([determineCoordinates(val) for val in args])
    except Exception as e:
        logging.error(e)
        logging.error("2Gis ключ устарел")
        return False


def getSight(address):
    global index_token
    x, y, ind = determineCoordinates(address)
    url = settings.getSights + f"q=Достопримечательность&sort_point={y},{x}&key={settings.keys[index_token]}"
    try:
        response = requests.get(url)
        mas = response.json()["result"]["items"][0:10]
        arr = []
        for val in mas:
            arr.append(val["full_name"])
        return arr
    except requests.exceptions.InvalidSchema:
        index_token += 1
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)
        return getSight(address)


def getRoute(args, way="multimodal"):
    url = f"https://2gis.ru/directions/points/"
    for val in args:
        url += f"{val[1]}%2C{val[0]}%3B{val[2]}" + "%7C"
    return url


def makeRoute(args):
    global index_token
    try:
        agents = [{"agent_id": 0, "start_waypoint_id": 0, "finish_waypoint_id": len(args) - 1}]
        waypoints = []
        for i in range(len(args)):
            coordinates = determineCoordinates(args[i])
            waypoints.append({"waypoint_id": i, "point": {"lat": coordinates[0], "lon": coordinates[1]}})
        task_id = requests.post(settings.makeOpt, json={"agents": agents, "waypoints": waypoints}).json()["task_id"]
        time.sleep(2.5)
        response = requests.get(settings.getRoute + f"{task_id}&key={settings.keys[index_token]}").json()
        response = response["urls"]["url_vrp_solution"]
        mas = []
        for val in requests.get(response).json()["routes"][0]["points"]:
            mas.append(args[val])
        return mas
    except KeyError:
        index_token += 1
        if index_token >= len(settings.keys):
            index_token -= len(settings.keys)
        makeRoute(args)


def split(start, end, ans):
    return [start] + ans.split("$") + [end]