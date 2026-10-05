import RPi.GPIO as GPIO
import time

LED_PIN = 17      # LED 腳位 (BCM GPIO17，實體腳位 11)，請依你的接線調整
BUZZER_PIN = 18   # 蜂鳴器腳位 (BCM GPIO18，實體腳位 12)，請依你的接線調整
freq = 523        # 蜂鳴器頻率 (523Hz，大約是 C5)

UNIT = 0.2        # 摩斯密碼基本時間單位 (秒)
DOT = UNIT        # 短 = 1 單位
DASH = UNIT * 3   # 長 = 3 單位
SYMBOL_GAP = UNIT       # 同一字母內，短/長之間間隔 1 單位
LETTER_GAP = UNIT * 3   # 字母之間間隔 3 單位
WORD_GAP = UNIT * 7     # 每次 SOS 之間間隔 7 單位

MORSE = {
    "S": "...",
    "O": "---",
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, freq)


def signal(duration):
    # 燈泡亮 + 蜂鳴器響，持續 duration 秒
    GPIO.output(LED_PIN, GPIO.HIGH)
    buzzer.start(50)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)
    buzzer.stop()


try:
    while True:
        for letter in "SOS":
            print(f"{letter}: {MORSE[letter]}")
            for symbol in MORSE[letter]:
                signal(DOT if symbol == "." else DASH)
                time.sleep(SYMBOL_GAP)
            time.sleep(LETTER_GAP - SYMBOL_GAP)
        time.sleep(WORD_GAP - LETTER_GAP)

except KeyboardInterrupt:
    pass
finally:
    buzzer.stop()
    GPIO.cleanup()
