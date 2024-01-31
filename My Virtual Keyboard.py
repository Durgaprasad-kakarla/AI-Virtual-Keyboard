import cv2
import time
import os
import HandTrackingModule as htm
from pynput.keyboard import Controller,Key
import cvzone

dic = {'`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
       '-': '_', '=': '+', '[': '{',
       ']': '}', ';': ':', ',': '<', '.': '>', '/': '?', "'": '"', '\\': "|"}


def drawAll(img, buttonList):
    for i, button in enumerate(buttonList):
        x, y = button.pos
        w, h = button.size
        if button.text == 'caps':
            print("caps", x, y, w, h)
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),colorC=(0,126,255), t=8, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED)
        if button.text in dic.keys():
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            cv2.putText(img, dic[button.text], (x + 3, y + 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        else:
            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)


class Button():
    def __init__(self, pos, text, size=[75, 80]):
        self.pos = pos
        self.size = size
        self.text = text


lst = []

text_x, text_y = 14, 50
pos_text = (text_x, text_y)
cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.8)

keys = [['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '<-'],
        ['tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
        ['caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'ent'],
        ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'shift']]
button_list = []
final_text = ['']
delayCounter = 0
keyboard = Controller()
for x, key in enumerate(keys):
    for i, C in enumerate(keys[x]):
        if x == 0 and i != len(keys[x]) - 1:
            button_list.append(Button([100 * i + 10, 100 * x + 100], C))
        elif i == 0 and x != 0:
            button_list.append(Button([100 * i + 10, 100 * x + 100], C, size=[170, 80]))
        elif i == len(keys[x]) - 1 and x == len(keys) - 1:
            button_list.append(Button([100 * i + 100, 100 * x + 100], C, size=[190, 80]))
        elif i == len(keys[x]) - 1 and x != 1:
            if x > 0:
                button_list.append(Button([100 * i + 100, 100 * x + 100], C, size=[180, 80]))
            else:
                button_list.append(Button([100 * i + 10, 100 * x + 100], C, size=[160, 80]))
        else:
            if x > 0:
                button_list.append(Button([100 * i + 100, 100 * x + 100], C))
            else:
                button_list.append(Button([100 * i + 150, 100 * x + 100], C))
cnt = 0
capital = 0
windows_img=cv2.imread("Main Logo (1).png")
windows_img=cv2.resize(windows_img,(50,50))
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1500, 700))
    hands, bboxInfo = detector.findHands(img,draw=False)
    drawAll(img, button_list)
    cv2.rectangle(img,(250,500),(330,575),(255, 255, 255),cv2.FILLED)
    cvzone.cornerRect(img, (250, 500, 80, 75),colorC=(0,126,255), t=3, rt=0)
    img[513:563,265:315]=windows_img
    cv2.rectangle(img, (350, 500), (1000, 575), (255, 255, 255), cv2.FILLED)
    if hands:
        print(hands)
        lmList = []
        lmListLe = []
        if len(hands) > 1:
            if hands[0]['type'] == 'Right':
                lmList = hands[0]['lmList']
                lmListLe = hands[1]['lmList']
            else:
                lmListLe = hands[0]['lmList']
                lmList = hands[1]['lmList']
        else:
            if hands[0]['type'] == 'Right':
                lmList = hands[0]['lmList']
            if hands[0]['type'] == 'Left':
                lmListLe = hands[0]['lmList']
        if hands:
            shift = 0
            if lmListLe:
                x1, y1, w1, h1 = 10, 400, 170, 80
                x2, y2, w2, h2 = 1200, 400, 190, 80
                if x1 < lmListLe[8][0] < x1 + w1 and y1 < lmListLe[8][1] < y1 + h1:
                    print(lmListLe[8])
                    l1, _, _ = detector.findDistance(lmListLe[8][:2], lmListLe[12][:2], img)
                    if l1 < 50:
                        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1),(0,126,255), cv2.FILLED)
                        cv2.putText(img, "shift", (x1 + 20, y1 + 65), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)
                        shift = 1
                if x2 < lmListLe[8][0] < x2 + w2 and y2 < lmListLe[8][1] < y2 + h2:
                    print(lmListLe[8])
                    l1, _, _ = detector.findDistance(lmListLe[8][:2], lmListLe[12][:2], img)
                    if l1 < 50:
                        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0,126,255), cv2.FILLED)
                        cv2.putText(img, "shift", (x2 + 20, y2 + 65), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)
                        shift = 1
            if lmList:
                x1, y1 = 350, 500
                w1, h1 = 650, 75
                if x1 < lmList[8][0] < x1 + w1 and y1 < lmList[8][1] < y1 + h1:
                    l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
                    if l < 50:
                        cv2.rectangle(img, (350, 500), (1000, 575), (0, 126, 255), cv2.FILLED)
                        if delayCounter == 0:
                            final_text[-1] += ' '
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                            delayCounter = 1
                x2,y2=250,500
                w2,h2=75,80
                if x2 < lmList[8][0] < x2 + w2 and y2 < lmList[8][1] < y2 + h2:
                    l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
                    if l < 50:
                        if delayCounter == 0:
                            cv2.rectangle(img, (250, 500), (330, 575), (0,126,255), cv2.FILLED)
                            keyboard.press(Key.cmd)
                            keyboard.release(Key.cmd)
                for button in button_list:
                    x, y = button.pos
                    w, h = button.size
                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
                        print(l)
                        if l < 50:
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0,126,255), cv2.FILLED)
                            if shift == 1 and button.text in dic:
                                cv2.putText(img, dic[button.text], (x + 20, y + 65), cv2.FONT_HERSHEY_COMPLEX, 2,
                                            (255, 255, 255), 6)
                            else:
                                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_COMPLEX, 2,
                                            (255, 255, 255), 6)
                            if delayCounter == 0:
                                if button.text == '<-':
                                    if final_text[-1] == '' and len(final_text) > 1:
                                        final_text.pop(-1)
                                    else:
                                        final = final_text.pop(-1)
                                        final_text.append(final[:-1])
                                    keyboard.press('\b')
                                    keyboard.release('\b')

                                elif button.text == 'ent':
                                    keyboard.press(Key.enter)
                                    keyboard.release(Key.enter)
                                    final_text.append('')
                                    cnt += 1
                                elif cnt >= 2:
                                    final_text = [button.text]
                                    cnt = 0
                                elif button.text == 'tab':
                                    final_text[-1] += '   '
                                    keyboard.press(Key.tab)
                                    keyboard.release(Key.tab)

                                elif button.text == 'shift':
                                    continue
                                elif button.text == 'caps':
                                    if capital == 0:
                                        capital = 1
                                    else:
                                        capital = 0
                                else:
                                    if capital == 0:
                                        if shift == 1:
                                            if button.text in dic:
                                                final_text[-1] += dic[button.text]
                                            else:
                                                final_text[-1] += (button.text)
                                        else:
                                            final_text[-1] += (button.text).lower()
                                    else:
                                        if shift == 1:
                                            if button.text in dic:
                                                final_text[-1] += dic[button.text]
                                            else:
                                                final_text[-1] += (button.text).lower()
                                        else:
                                            final_text[-1] += button.text
                                    if button.text!='tab':
                                        keyboard.press(final_text[-1][-1])
                                delayCounter = 1
    if capital==1:
        cv2.circle(img, (170, 310), 9, (0, 255, 0), cv2.FILLED)
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
    text_x, text_y = pos_text
    val = 0
    cv2.rectangle(img, (10, 15), (1480, 90), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (10, 15), (1480, 90), (0,0,0), 3)
    if final_text:
        for txt in final_text:
            cv2.putText(img, txt, (text_x, text_y + val), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)
            val += 28
    cvzone.cornerRect(img, (350, 500, 650, 75),colorC=(0,126,255),t=5, rt=0)
    # img=cv2.resize(img,(900,600))
    cv2.imshow("AI Virtual Keyboard", img)
    cv2.waitKey(1)
