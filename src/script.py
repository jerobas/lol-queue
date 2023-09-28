import subprocess
import re
import base64
import websocket
import json
import ssl
import requests
from utils.champions import get_champions, find_similar_name
from services.champion import checkIfBansavailable


command_string = "wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline"


def check_gameflow(token, port):
    notOnChampionSelection = True
    while notOnChampionSelection:
        res = requests.get(f"https://127.0.0.1:{port}/lol-gameflow/v1/gameflow-phase",
                           headers={"Authorization": f"Basic {token}"},
                           verify=False,
                           )
        if res.text == "ChampSelect":
            notOnChampionSelection = False
            return True


def handle_on_gameflow_phase_change(token, port, idPickName, idBanName):
    def on_gameflow_phase_change(ws, message):
        print(message[2]["data"])
        match message[2]["data"]:
            case "ChampSelect":
                checkIfBansavailable(token, port, idPickName, idBanName) 
            case "ReadyCheck":
                print("phase: ReadyCheck")
                res = requests.post(
                    f"https://127.0.0.1:{port}/lol-lobby-team-builder/v1/ready-check/accept",
                    headers={"Authorization": f"Basic {token}"},
                    verify=False,
                )
                print(res.text)
            case "Lobby":
                print("phase: Lobby")
            case _:
                print("No match")

    return on_gameflow_phase_change


def on_open(ws):
    ws.send(json.dumps([5, "OnJsonApiEvent_lol-gameflow_v1_gameflow-phase"]))


def on_error(ws, error):
    print(error)
    ws.close()


def main(pickName="None", banName="None"):
    idPickName = 99 
    idBanName = 157
    output = subprocess.check_output(command_string.split()).decode("utf-8")

    password = re.search("--remoting-auth-token=([\w-]*)", output).group(1)
    token = base64.b64encode(
        f"riot:{password}".encode("utf-8")).decode("utf-8")

    port = re.search("--app-port=([0-9]*)", output).group(1)
    
    champions = get_champions(token, port)
    
    if pickName != "None":
        print(pickName)
        idPickName = find_similar_name(pickName, champions)
    if banName != "None":
        print(banName)
        idBanName = find_similar_name(banName, champions)
    print(idPickName, idBanName)
    on_gameflow_phase_change = handle_on_gameflow_phase_change(token, port, idPickName, idBanName)

    def on_message(ws, message):
        message = json.loads(message)
        match message[1]:
            case "OnJsonApiEvent_lol-gameflow_v1_gameflow-phase":
                on_gameflow_phase_change(ws, message)

    websocket.enableTrace(True)
    wsapp = websocket.WebSocketApp(
        f"wss://localhost:{port}",
        subprotocols=["wamp"],
        header={
            "Authorization": f"Basic {token}",
        },
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=lambda ws: print("connection closed"),
    )

    wsapp.run_forever(
        sslopt={"cert_reqs": ssl.CERT_NONE}, suppress_origin=True)

