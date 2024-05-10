keys = [
        "62d0d797-2d57-416c-add8-4758500d9e5a",
        "c798f9b7-95e0-4228-ac87-9dff6cfd37d7",
        "96c125fc-c1d0-499f-bd63-f574b9996c83",
        "79552add-3a03-49bf-a5d0-0f9b33e92118",
        "90b9ccf1-33a7-4c35-accb-36225d1a2db6",
        "0b939a1e-92dd-48b2-bc18-32aeec793341",
        "d6eac903-d3d2-45f0-8345-981f03a9c39a",
]
getSights = f"https://catalog.api.2gis.com/3.0/items?"
makeOpt = f"https://routing.api.2gis.com/logistics/vrp/1.1.0/create?key="
getRoute = "https://routing.api.2gis.com/logistics/vrp/1.1.0/status?task_id="
idf = "Y2I5NzU5ZTMtMTZhMy00YzhmLTgwODAtNTAwZWQ1ZGEwYzMzOjU0YmY4ZjQwLWI5NTgtNDJiNi1iZGVjLWRhODI5MTY5NWEzMg=="
telebot_token = "7131622872:AAF1NpdTKCUExxmwt2_bC5VmOlyRxD6BpXA"
def makeLink(l):
        return f'<a href="{l}">Ссылка на 2гис</a>'