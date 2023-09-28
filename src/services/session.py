import requests


def get_sessionData(token, port):
    res = requests.get(f'https://127.0.0.1:{port}/lol-champ-select/v1/session',
                       headers={"Authorization": f"Basic {token}"},
                       verify=False
                       )
    return res
