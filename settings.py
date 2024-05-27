import os

emmbedding_model_name = "intfloat/multilingual-e5-base"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_file_for_embeddings = os.path.join(ROOT_DIR, "DataBase", "res1.csv")
FAISS_FOLDER = 'faiss_index'
keys = [
        "62d0d797-2d57-416c-add8-4758500d9e5a",
        "c798f9b7-95e0-4228-ac87-9dff6cfd37d7",
        "96c125fc-c1d0-499f-bd63-f574b9996c83",
        "79552add-3a03-49bf-a5d0-0f9b33e92118",
        "90b9ccf1-33a7-4c35-accb-36225d1a2db6",
        "0b939a1e-92dd-48b2-bc18-32aeec793341",
]
getSights = f"https://catalog.api.2gis.com/3.0/items?"
makeOpt = f"https://routing.api.2gis.com/logistics/vrp/1.1.0/create?key="
getRoute = "https://routing.api.2gis.com/logistics/vrp/1.1.0/status?task_id="
idf = "Y2I5NzU5ZTMtMTZhMy00YzhmLTgwODAtNTAwZWQ1ZGEwYzMzOjU0YmY4ZjQwLWI5NTgtNDJiNi1iZGVjLWRhODI5MTY5NWEzMg=="
telebot_token = "7131622872:AAF1NpdTKCUExxmwt2_bC5VmOlyRxD6BpXA"

url_giga_get_token = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
payload = 'scope=GIGACHAT_API_PERS'
model_params = {
            "model": "GigaChat",
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1
        }

def makeLink(l):
        return f'<a href="{l}">Ссылка на 2гис</a>'