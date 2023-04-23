import requests
import json
from .models import Juntuan


class CharacterInfo:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name



class IdsRes:
    def __init__(self, characters=None):
        self.characters = characters or []

class Esi:


    def get_ids(character_names):
        base_url = "https://esi.evepc.163.com/latest"
        headers = {"User-Agent": "Esi"}
        url = f"{base_url}/universe/ids/?datasource=infinity&language=zh"
        headers = {
            "accept": "application/json",
            "Accept-Language": "zh",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

        data =  [character_names]
        response = requests.post(url,headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            ids_res = IdsRes(**response.json())

            characters = ids_res.characters

            character_ids = [c['id'] for c in characters]
            url = f"{base_url}/characters/affiliation/"
            params = {"datasource": "infinity"}
            data = character_ids
            response = requests.post(url, headers=headers, params=params, json=data)
            if response.status_code == 200:
                result = response.json()

                affiliations = result
                res = []
                for i, c in enumerate(characters):

                    affiliation = affiliations[i]
                    corporation_id = affiliation["corporation_id"]
                    info = CharacterInfo(id=c['id'], name=c['name'])
                    info.corporation_id = corporation_id

                    if Juntuan.objects.filter(juntuan_id = corporation_id).exists():
                        res.append(info)
                    else:
                        url = "https://esi.evepc.163.com/latest/universe/names/?datasource=infinity"
                        data = [corporation_id]
                        headers = {
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Cache-Control": "no-cache"
                        }
                        response = requests.post(url, headers=headers, data=json.dumps(data))

                        if response.status_code == 200:
                            result = response.json()
                            info.corporation_name =result[0]['name']
                            res.append(info)
                        else:
                            return None

                return res
            else:
                return None
        else:
            return None

