from pyautogui import *
import pyautogui
import os
from time import sleep
import ssl

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
script_dir = os.path.dirname(__file__)
cert_path = os.path.join(script_dir, 'certs', 'certfile.pem')
context.load_cert_chain(cert_path)
image_path = os.path.join(script_dir, 'assets', 'accept.png')

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(x ,y)
    
def checkScreen():
    button_pos = pyautogui.locateOnScreen(image_path)

    if button_pos != None:
        click(button_pos.left, button_pos.top)
        print('Match found!')
        return False
    else:
        return True

def main():
    print('If i find a match i will accept it for you...',  end="\n")
    
    while True: 
        if checkScreen() == False: 
            break
        else:
            sleep(4)

main()            