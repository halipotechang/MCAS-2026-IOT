import os
import sys
import time
import serial

# 使用 Lab3/7segment_display/raspberrypi-tm1637 裡的 tm1637.py
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "Lab3", "7segment_display", "raspberrypi-tm1637"))

import RPi.GPIO as GPIO
from tm1637 import TM1637

# UART 自己傳給自己（loopback）：TXD GPIO14（實體腳位 8）用杜邦線接 RXD GPIO15（實體腳位 10）
# 七段顯示器 TM1637：CLK 接 BCM GPIO5（實體腳位 29）、DIO 接 BCM GPIO4（實體腳位 7）
CLK = 5
DIO = 4

# 輪流傳送的數字與字元（七段顯示器最多 4 個字，只能顯示 0-9、A-Z、空白、-）
MESSAGES = ["1234", "HI", "LAB4", "2026", "N971", "-OK-"]

# 設定 UART 連接埠與參數（預設使用 /dev/serial0）
ser = serial.Serial(
    port='/dev/serial0',      # 對應 GPIO14 (TX) 和 GPIO15 (RX)
    baudrate=9600,            # 傳輸速率
    timeout=1                 # 讀取逾時設定（秒）
)

tm = TM1637(clk=CLK, dio=DIO)
tm.brightness(3)


# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write((data + "\n").encode('utf-8'))
        print(f"已傳送：{data}")


# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode('utf-8').strip()
        if incoming:
            print(f"收到資料：{incoming}")
        return incoming


# 把收到的資料顯示在七段顯示器上
def show_on_led(text):
    text = text.upper()[:4].ljust(4)  # 補滿 4 格，靠左顯示
    try:
        tm.show(text)
    except ValueError:
        tm.show("ERR ")  # 有七段顯示器顯示不出來的字元


# 主程式
try:
    i = 0
    while True:
        send_data(MESSAGES[i % len(MESSAGES)])
        time.sleep(0.1)
        data = receive_data()
        if data:
            show_on_led(data)
        else:
            print("沒有收到資料，請檢查 TX/RX 接線")
            tm.show("----")
        i += 1
        time.sleep(1.5)

except KeyboardInterrupt:
    print("程式中斷")

finally:
    if ser.is_open:
        ser.close()
        print("串列埠已關閉")
    tm.write([0, 0, 0, 0])
    GPIO.cleanup()
