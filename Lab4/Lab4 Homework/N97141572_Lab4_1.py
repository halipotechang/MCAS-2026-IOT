import time
import adafruit_dht
import board

# DHT11：VCC 接 5V（實體腳位 2）、DATA 接 BCM GPIO4（實體腳位 7）、GND 接地（實體腳位 6）
dht_device = adafruit_dht.DHT11(board.D4)  # GPIO4

try:
    while True:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = dht_device.humidity

            print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
        except RuntimeError as err:
            # DHT11 偶爾會讀取失敗（例如 Checksum did not validate），印出錯誤後繼續讀
            print(err.args[0])

        time.sleep(2.0)

except KeyboardInterrupt:
    print("\n停止讀取")
finally:
    dht_device.exit()
