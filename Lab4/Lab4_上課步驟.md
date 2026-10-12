# Lab4 上課步驟清單（DHT11 / HC-SR04 / UART）

作業程式已寫好，放在 `Lab4/Lab4 Homework/`：

| 題目 | 檔案 | 要截圖 |
|---|---|---|
| 4-1 DHT11 溫溼度 | `N97141572_Lab4_1.py` | ✅ |
| 4-2 HC-SR04 倒車雷達 | `N97141572_Lab4_2.py` | ✅ |
| 4-3 UART 傳輸 + 七段顯示器 | `N97141572_Lab4_3.py` | ✅ |

---

## 0. 上課前（在 Mac 上）

- [x] 作業程式、`requirements.txt` 和這份清單都已經 push 到自己的 GitHub fork

## 1. 樹莓派準備

- [ ] 把 repo 抓到樹莓派上（第一次用 clone，之前 clone 過就用 pull）
  ```bash
  git clone https://github.com/halipotechang/MCAS-2026-IOT.git   # 第一次
  cd MCAS-2026-IOT && git pull                                    # 之後
  ```
- [ ] 安裝編譯工具
  ```bash
  sudo apt install swig liblgpio-dev
  ```
- [ ] 在 Lab4 資料夾建立虛擬環境並啟用
  ```bash
  cd MCAS-2026-IOT/Lab4
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] 依 `requirements.txt` 安裝 Python 套件（清單裡的 `pyserial` 是 4-3 要用的，投影片沒有寫）
  ```bash
  python3 -m pip install -r requirements.txt
  ```
  > venv 不能從 Mac 帶過來，必須在樹莓派上建立。同一台樹莓派只要建過一次，之後直接 `source venv/bin/activate` 就能用，不用重裝。
- [ ] 確認終端機提示字元有顯示學號（截圖要看得到）

> 每次開新的終端機都要重新 `source venv/bin/activate`，提示字元前面出現 `(venv)` 才算啟用。

---

## 2. Lab 4-1：DHT11 溫溼度

**接線**（請先關機或拔電再接線）

| DHT11 | 樹莓派 |
|---|---|
| VCC（+） | 5V（實體腳位 2） |
| DATA（S） | GPIO4（實體腳位 7） |
| GND（−） | GND（實體腳位 6） |

> 不同 DHT11 模組的腳位順序可能不一樣，請以模組上印的標示為準。

**執行**
```bash
cd "Lab4 Homework"
python N97141572_Lab4_1.py
```

**預期輸出**
```
Temp:26.2 C / 79.2 F    Humidity: 44%
Checksum did not validate. Try again.   ← 偶爾出現是正常的
```

- [ ] 截圖，存成 `N97141572_Lab4_1.png`
- [ ] 按 Ctrl+C 結束程式

---

## 3. Lab 4-2：HC-SR04 倒車雷達

**接線**

| HC-SR04 | 樹莓派 |
|---|---|
| Vcc | 5V（實體腳位 4） |
| Trig | GPIO23（實體腳位 16） |
| Echo | GPIO24（實體腳位 18） |
| Gnd | GND（實體腳位 14） |

> Echo 腳輸出的是 5V，樹莓派 GPIO 只能接受 3.3V。比較保險的接法是用 1kΩ＋2kΩ 電阻分壓。

**執行**
```bash
python N97141572_Lab4_2.py
```

**預期輸出**（用手在感測器前面前後移動）
```
目前距離：16.62 cm
注意！！！
目前距離：39.21 cm
沒事
```

- [ ] 截圖時，畫面要同時有「注意！！！」和「沒事」，存成 `N97141572_Lab4_2.png`
- [ ] 按 Ctrl+C 結束程式

**疑難排解**：程式卡住、沒有任何輸出，通常是 Trig 和 Echo 接反，或 Echo 沒接好。

---

## 4. Lab 4-3：UART 自己傳給自己，並顯示在七段顯示器

**啟用 UART**（只需要做一次）
```bash
sudo raspi-config
```
- [ ] 3 Interface Options → I6 Serial Port
- [ ] login shell over serial? → **No**
- [ ] serial port hardware enabled? → **Yes**
- [ ] 重開機後，回到 Lab4 資料夾重新 `source venv/bin/activate`

**接線**

| 元件 | 樹莓派 |
|---|---|
| 杜邦線一端接 TXD | GPIO14（實體腳位 8） |
| 杜邦線另一端接 RXD | GPIO15（實體腳位 10） |
| TM1637 CLK | GPIO5（實體腳位 29） |
| TM1637 DIO | GPIO4（實體腳位 7） |
| TM1637 VCC / GND | 5V / GND |

> 4-3 的 DIO 跟 4-1 的 DHT11 用同一支 GPIO4，做 4-3 前要先把 DHT11 拔掉。

**執行**
```bash
python N97141572_Lab4_3.py
```

**預期輸出**：七段顯示器會輪流顯示 `1234 → HI → LAB4 → 2026 → N971 → -OK-`
```
已傳送：1234
收到資料：1234
已傳送：HI
收到資料：HI
```

- [ ] 截圖，存成 `N97141572_Lab4_3.png`；建議也拍一張七段顯示器的照片
- [ ] 按 Ctrl+C 結束程式

**疑難排解**
- 一直出現「沒有收到資料」：檢查腳位 8 和 10 的接線，以及 raspi-config 有沒有啟用。
- `No module named 'serial'`：venv 沒有啟用，或還沒裝 `pyserial`。
- `/dev/serial0` 不存在：UART 沒啟用，或啟用後沒有重開機。

---

## 5. 繳交

- [ ] `Lab4 Homework/` 裡要有 6 個檔案：3 個 `.py` 和 3 張截圖
- [ ] 把截圖傳回 repo，然後 push
  ```bash
  cd ~/MCAS-2026-IOT     # 依你 clone 的位置調整
  git add "Lab4/Lab4 Homework"
  git commit -m "Add Lab4 screenshots"
  git push origin main
  ```
  > 樹莓派上 push 需要登入 GitHub。如果沒辦法登入，就把截圖傳回 Mac，再從 Mac push。
- [ ] 到 Moodle 繳交 GitHub 連結：https://github.com/halipotechang/MCAS-2026-IOT/tree/main/Lab4/Lab4%20Homework
