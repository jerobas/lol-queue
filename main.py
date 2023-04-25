from pyautogui import *
import pyautogui
from time import sleep

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(x ,y)
    
def checkScreen():
    button_pos = pyautogui.locateOnScreen('./accept.png')

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