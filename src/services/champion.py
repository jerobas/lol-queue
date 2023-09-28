import json
import requests

from .session import get_sessionData

HTTP_OK = (200, 204)


def checkIfBansavailable(token, port, idPickName, idBanName):
    session_data = get_sessionData(token, port)
    if session_data.status_code not in HTTP_OK:
        return
    session_data_json = json.loads(session_data.text)
    action = session_data_json.get("actions", [[]])[0][0]
    id = action.get("id")
    if action.get("type") == 'ban' and idBanName != "None":
        ban_champion(token, port, id, idBanName, idPickName)
    if action.get("type") == 'pick':
        pick_champion(token, port, id, idPickName)
    else:
        checkIfBansavailable(token, port, idPickName, idBanName)


def ban_champion(token, port, id, idPickName, idBanName):
    res = requests.patch(f'https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{id}',
                         headers={
                             "Authorization": f"Basic {token}"},
                         verify=False,
                         json={'championId': idBanName},
                         data=''
                         )
    if res.status_code == 204 or res.status_code == 200:
        res = requests.post(f'https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{id}/complete',
                            headers={
                                "Authorization": f"Basic {token}"},
                            verify=False,
                            json={'championId': idBanName},
                            data=''
                            )
        if res.status_code == 204 or res.status_code == 200:
            checkIfBansavailable(token, port, idPickName, idBanName)


def pick_champion(token, port, id, idPickName=99):
    res = requests.patch(f'https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{id}',
                         headers={"Authorization": f"Basic {token}"},
                         verify=False,
                         json={'championId': idPickName},
                         data=''
                         )
    if res.status_code == 204 or res.status_code == 200:
        res = requests.post(f'https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{id}/complete',
                            headers={"Authorization": f"Basic {token}"},
                            verify=False,
                            json={'championId': idPickName},
                            data=''
                            )
        if res.status_code == 204 or res.status_code == 200:
            pass
