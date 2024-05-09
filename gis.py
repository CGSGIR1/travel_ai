import requests
import settings
import time
import logging
logging.basicConfig(level=logging.INFO)


def determineCoordinates(adress):
    # Ф-я для определения координат точки
    resp_url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={adress}&fields=items.point&key={settings.key}"
    response = requests.get(resp_url)
    lat = response.json()["result"]["items"][0]["point"]["lat"]
    lon = response.json()["result"]["items"][0]["point"]["lon"]
    id = response.json()["result"]["items"][0]["id"]
    return [lat, lon, id]


def getLink(attrAdresses, *args):
    try:
        args = [args[0]] + getAdressForAttracitons(attrAdresses) + [args[1]]
        return getRoute([determineCoordinates(val) for val in args])
    except Exception as e:
        logging.error(e)
        logging.error("2Gis ключ устарел")
        return False


def getSight(address):
    x, y, ind = determineCoordinates(address)
    url = settings.getSights + f"q=Достопримечательность&sort_point={y},{x}&key={settings.key}"
    try:
        response = requests.get(url)
        mas = response.json()["result"]["items"][0:10]
        arr = []
        for val in mas:
            arr.append(val["full_name"])
        return arr
    except requests.exceptions.InvalidSchema:
        return {"status": "400"}


def getRoute(args, way="multimodal"):
    url = f"https://2gis.ru/directions/points/"
    for val in args:
        url += f"{val[1]}%2C{val[0]}" + "%7C"
    return url


def makeRoute(args):
    try:
        agents = [{"agent_id": 0, "start_waypoint_id": 0, "finish_waypoint_id": len(args) - 1}]
        waypoints = []
        for i in range(len(args)):
            coordinates = determineCoordinates(args[i])
            waypoints.append({"waypoint_id": i, "point": {"lat": coordinates[0], "lon": coordinates[1]}})
        task_id = requests.post(settings.makeOpt, json={"agents": agents, "waypoints": waypoints}).json()["task_id"]
        time.sleep(2.5)
        response = requests.get(settings.getRoute + f"{task_id}&key={settings.add}").json()
        response = response["urls"]["url_vrp_solution"]
        mas = []
        for val in requests.get(response).json()["routes"][0]["points"]:
            mas.append(args[val])
        return mas
    except KeyError:
        return {"status": "411"}
def getAdressForAttracitons(gig_answer):
    return gig_answer.split("$")
print(getLink("Москва-сити$Кремль$ВДНХ", "Санкт-Петербург", "Москва"))