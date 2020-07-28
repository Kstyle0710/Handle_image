### pip install Pillow

from PIL import ImageGrab
import time

time.sleep(5)   # 사용자가 동영상 틀 준비하는 시간 5초

# 2초 간격으로 10개 이지미 저장
for i in range(1, 11):
    img = ImageGrab.grab()  # 현재 스크린 이미지를 가져옮
    img.save("./screenshot/image_{0}.png".format(i))
    time.sleep(2)




