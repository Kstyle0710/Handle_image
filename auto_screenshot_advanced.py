## pip install keyboard
from PIL import ImageGrab
import time
import keyboard
import tkinter.messagebox as msgbox

def screenshot():
    curr_time = time.strftime("%Y%m%d_%H%M%S")
    img = ImageGrab.grab()     ## bbox(0, 0, 300, 300) 식으로 캡쳐 영역을 지정할 수도 있다.
    img.save("./screenshot/image_{0}.png".format(curr_time))

keyboard.add_hotkey("F9", screenshot)

keyboard.wait("esc")
msgbox.showinfo("알림", "작업이 완료되었습니다.")
