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

    def get_names(id_list):
        base_url = "https://esi.evepc.163.com/latest/universe/names/?datasource=infinity"
        headers = {
            "accept": "application/json",
            "Accept-Language": "zh",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
        data = id_list
        response = requests.post(base_url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result


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

        data =  character_names

        response = requests.post(url,headers=headers, json=data)


        if response.status_code == 200:
            ids_res = response.json()['characters']

            characters = ids_res
            char_dict = {item['id']:item['name'] for item in characters}

            character_ids = [c['id'] for c in characters]
            print(character_ids)
            url = f"{base_url}/characters/affiliation/"
            params = {"datasource": "infinity"}
            data = character_ids
            response = requests.post(url, headers=headers, params=params, json=data)
            if response.status_code == 200:
                result = response.json()

                affiliations = result
                res = []
                corp_list = []
                for i, c in enumerate(affiliations):

                    affiliation = affiliations[i]
                    corporation_id = affiliation["corporation_id"]
                    corp_list.append(corporation_id)
                    id = affiliation['character_id']
                    info = CharacterInfo(id=id, name=char_dict[id])
                    # info = CharacterInfo(id=c['id'], name=c['name'])
                    info.corporation_id = corporation_id
                    res.append(info)

                print(corp_list)
                existing_corp = Juntuan.objects.filter(name__in = corp_list).values_list('juntuan_id',flat=True)
                non_existing_corp = list(set(corp_list)- set(existing_corp))
                print(non_existing_corp)
                non_existing_corp_info = Esi.get_names(non_existing_corp)
                for corp in non_existing_corp_info:

                    juntuan_task = Juntuan(juntuan_id = corp['id'],name = corp['name'])
                    juntuan_task.save()

                return res
            else:
                return None
        else:
            return None



        #             if Juntuan.objects.filter(juntuan_id = corporation_id).exists():
        #                 res.append(info)
        #             else:
        #                 url = "https://esi.evepc.163.com/latest/universe/names/?datasource=infinity"
        #                 data = [corporation_id]
        #                 headers = {
        #                     "accept": "application/json",
        #                     "Content-Type": "application/json",
        #                     "Cache-Control": "no-cache"
        #                 }
        #                 response = requests.post(url, headers=headers, data=json.dumps(data))
        #
        #                 if response.status_code == 200:
        #                     result = response.json()
        #                     info.corporation_name =result[0]['name']
        #                     res.append(info)
        #                 else:
        #                     return None
        #
        #         return res
        #     else:
        #         return None
        # else:
        #     return None

