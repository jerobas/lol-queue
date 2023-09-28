import json
import requests


def get_champions(token, port):
    res = requests.get(f"https://127.0.0.1:{port}/lol-champions/v1/owned-champions-minimal",
                       headers={"Authorization": f"Basic {token}"},
                       verify=False,
                       )
    resWithReplace = res.text.replace('\\"', '"')
    resultado = [{'id': item['id'], 'name': item['name']}
                 for item in json.loads(resWithReplace)]
    champions_dict = {champion["name"].lower(): champion["id"]
                      for champion in resultado}
    return champions_dict


def find_similar_name(name, champions_dict):
    for champion_name, champion_id in champions_dict.items():
        if name.lower() in champion_name:
            return champion_id
    return None, None
