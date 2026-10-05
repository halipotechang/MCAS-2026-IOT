import RPi.GPIO as GPIO
import time

PIN = 11       # LED 實體腳位 11 (BCM GPIO17)
PIN2 = 12      # 蜂鳴器實體腳位 12 (BCM GPIO18)
freq = 523     # 頻率 (523Hz，大約是 C5)

UNIT = 0.2         # 摩斯密碼基本時間單位 (秒)
DOT = UNIT         # 短 = 1 單位
DASH = UNIT * 3    # 長 = 3 單位

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)

# 建立 PWM 物件，設定頻率 freq
voice = GPIO.PWM(PIN2, freq)


def beep(duration):
    GPIO.output(PIN, True)    # LED 亮
    voice.start(50)           # duty 50%，發聲
    time.sleep(duration)
    GPIO.output(PIN, False)   # LED 滅
    voice.stop()              # 停止發聲
    time.sleep(UNIT)          # 短/長之間間隔 1 單位


try:
    while True:
        print("S: ...")
        for i in range(3):
            beep(DOT)
        time.sleep(UNIT * 2)  # 字母間隔 3 單位 (beep 內已停 1 單位)

        print("O: ---")
        for i in range(3):
            beep(DASH)
        time.sleep(UNIT * 2)

        print("S: ...")
        for i in range(3):
            beep(DOT)
        time.sleep(UNIT * 6)  # 每次 SOS 之間間隔 7 單位

except KeyboardInterrupt:
    pass
finally:
    voice.stop()
    GPIO.cleanup()
