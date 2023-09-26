import subprocess, re, base64, websocket, json, ssl, requests

command_string = "wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline"


def handle_on_gameflow_phase_change(token, port):
    def on_gameflow_phase_change(ws, message):
        print(message[2], message[2]["data"])
        if message[2]["data"] == "ReadyCheck":
            print("Accepting ready check")
            res = requests.post(
                f"https://127.0.0.1:{port}/lol-lobby-team-builder/v1/ready-check/accept",
                headers={"Authorization": f"Basic {token}"},
                verify=False,
            )
            print(res, res.status_code, res.text)

    return on_gameflow_phase_change


def on_open(ws):
    print("connection opened")
    ws.send(json.dumps([5, "OnJsonApiEvent_lol-gameflow_v1_gameflow-phase"]))


def on_error(ws, error):
    print(error)
    ws.close()


def main():
    output = subprocess.check_output(command_string.split()).decode("utf-8")

    password = re.search("--remoting-auth-token=([\w-]*)", output).group(1)
    token = base64.b64encode(f"riot:{password}".encode("utf-8")).decode("utf-8")

    port = re.search("--app-port=([0-9]*)", output).group(1)

    on_gameflow_phase_change = handle_on_gameflow_phase_change(token, port)

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
    wsapp.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, suppress_origin=True)


if __name__ == "__main__":
    main()
