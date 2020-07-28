## pip install keyboard
from PIL import ImageGrab
import time
import keyboard

def screenshot():
    curr_time = time.strftime("%Y%m%d_%H%M%S")
    img = ImageGrab.grab()
    img.save("./screenshot/image_{0}.png".format(curr_time))

keyboard.add_hotkey("F9", screenshot)

keyboard.wait("esc")