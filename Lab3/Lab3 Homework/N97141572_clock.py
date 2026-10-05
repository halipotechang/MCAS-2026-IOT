import os
import sys
from time import sleep, localtime

# 使用 Lab3/7segment_display/raspberrypi-tm1637 裡的 tm1637.py
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "7segment_display", "raspberrypi-tm1637"))

import RPi.GPIO as GPIO
from tm1637 import TM1637

CLK = 5    # 依投影片接線：BCM GPIO5（實體腳位 29）
DIO = 4    # 依投影片接線：BCM GPIO4（實體腳位 7）

tm = TM1637(clk=CLK, dio=DIO)
tm.brightness(3)

try:
    while True:
        t = localtime()
        # 前半秒顯示冒號，後半秒熄滅 → 冒號每秒閃一下
        tm.numbers(t.tm_hour, t.tm_min, True)
        sleep(0.5)
        tm.numbers(t.tm_hour, t.tm_min, False)
        sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    tm.write([0, 0, 0, 0])
    GPIO.cleanup()
