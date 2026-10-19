# Lab5 上課步驟清單（WebSocket / ZeroMQ / LLM API）

這次的分工：**筆電（Mac）當 Client／Publisher，樹莓派當 Server／Subscriber**。兩台要連在同一個網路。

| 題目 | 筆電執行 | 樹莓派執行 | 要截圖 |
|---|---|---|---|
| Task 1 WebSocket 傳指令 | `01_WebSocket/client.py` | `01_WebSocket/server.py` | 樹莓派 Server 收到 `on` 和 `off` |
| Task 2 ZeroMQ 傳影像 | `02_ZeroMQ/publisher.py` | `02_ZeroMQ/subscriber.py` | 瀏覽器顯示筆電鏡頭的畫面 |
| Task 3 LLM 轉成指令再傳送 | `03_LLM_WebSocket/client_llm.py` | `03_LLM_WebSocket/server.py` | LLM 輸出的指令＋樹莓派 Server 收到的畫面 |

> 截圖要放進**各題自己的資料夾**（`01_WebSocket/`、`02_ZeroMQ/`、`03_LLM_WebSocket/`），然後 push 到 GitHub。

---

## 0. 環境準備

### 0-1 取得最新的 Lab5
- [x] Mac：已經合併老師的 upstream，`Lab5/` 已經在 repo 裡
- [ ] 樹莓派：把最新版本拉下來（路徑依你 clone 的位置調整；投影片用的是 `~/lab/MCAS-2026-IOT`）
  ```bash
  cd ~/lab/MCAS-2026-IOT
  git pull
  ```

### 0-2 樹莓派建立 Lab5 虛擬環境（只要做一次）
- [ ] 建立虛擬環境並安裝套件
  ```bash
  cd ~/lab/MCAS-2026-IOT/Lab5
  python3 -m venv venv
  source venv/bin/activate
  python -m pip install -r requirements.txt
  python -m pip show websockets      # 有看到版本資訊就代表安裝成功
  ```
- 之後每次開新的終端機，只要執行下面兩行：
  ```bash
  cd ~/lab/MCAS-2026-IOT/Lab5
  source venv/bin/activate
  ```

### 0-3 筆電（Mac）建立虛擬環境
投影片寫的是 Windows 的 `py` 指令，Mac 要改用 `python3`。
- [x] 在 Mac 的 repo 裡直接建立虛擬環境（`requirements_pc.txt` 已經在資料夾裡，不用另外複製）。已經裝好，另外多裝了 Flask，用來在 Mac 上自己測試；上課時只要 `source venv/bin/activate`
  ```bash
  cd ~/Documents/MCAS-2026-IOT/Lab5
  python3 -m venv venv
  source venv/bin/activate
  python -m pip install -r requirements_pc.txt
  ```
  > 投影片 Task 1 寫的是 `websockets==17.1`，但 `requirements_pc.txt` 寫的是 `16.0`。照 requirements 裝就可以，兩個版本都支援程式用到的 `websockets.sync`。

### 0-4 查詢兩台的 IP
- [ ] 樹莓派 IP（Task 1、Task 3 會用到）：`hostname -I`
- [ ] Mac IP（Task 2 會用到）：`ipconfig getifaddr en0`
  > 要和樹莓派在同一個網段。例如兩台都是 `192.168.x.x`，前三段要一樣。

---

## 1. Task 1：WebSocket 指令傳輸（port 8765）

**樹莓派：啟動 Server**
```bash
cd ~/lab/MCAS-2026-IOT/Lab5/01_WebSocket
python server.py
```
預期輸出：
```
=== WebSocket Server ===
Listening on ws://0.0.0.0:8765
Waiting for client...
```

**Mac：啟動 Client**
```bash
cd ~/Documents/MCAS-2026-IOT/Lab5/01_WebSocket
python client.py
```
- [ ] 輸入樹莓派的 IP
- [ ] 依序輸入指令：`on`、`off`、`status`，最後輸入 `quit` 離開

樹莓派預期輸出：
```
[CONNECTED] 192.168.x.x:xxxxx
[RECEIVED] on
[SENT] OK: Device ON
[RECEIVED] off
[SENT] OK: Device OFF
```

- [ ] **截圖**：樹莓派 Server 收到 `on` 和 `off` 的畫面，存到 `01_WebSocket/`
- [ ] 在樹莓派按 Ctrl+C 停止 Server

---

## 2. Task 2：ZeroMQ 影像傳輸（ZMQ port 5555，網頁 port 5000）

資料流向：Mac 鏡頭 → ZeroMQ PUB → 樹莓派 SUB → Flask 網頁 → 瀏覽器

**Mac：啟動 Publisher**
```bash
cd ~/Documents/MCAS-2026-IOT/Lab5/02_ZeroMQ
python publisher.py
```
預期輸出：
```
=== ZeroMQ Publisher ===
Publishing on tcp://0.0.0.0:5555
Opening camera...
Camera opened.
Sending frames... Press Ctrl+C to stop.
```
> **Mac 常見問題**
> - 第一次執行時，macOS 會詢問是否允許終端機使用相機，要選**允許**。如果出現 `ERROR: Cannot open camera.`，到「系統設定 → 隱私權與安全性 → 相機」開啟 Terminal（或 iTerm、VS Code）的權限，重開終端機後再執行一次。
> - 如果跳出「是否允許 python 接受連入連線」，選**允許**，否則樹莓派連不進來。

> 在 Mac 上自己測 subscriber 時，5000 port 會被 AirPlay 接收器佔用，出現 `Address already in use`。上課時 subscriber 是在樹莓派上執行，不會有這個問題。

**樹莓派：啟動 Subscriber**
```bash
cd ~/lab/MCAS-2026-IOT/Lab5/02_ZeroMQ
python subscriber.py
```
- [ ] 輸入 **Mac 的 IP**（注意這題要輸入的是筆電 IP，不是樹莓派 IP）

預期輸出：
```
=== ZeroMQ Subscriber ===
Connected to publisher: tcp://192.168.x.x:5555
Receiving frames...
=== Browser Viewer ===
請在瀏覽器開啟：http://<樹莓派IP>:5000
```

**Mac：用瀏覽器查看**
- [ ] 用 Chrome 或 Safari 開啟 `http://<樹莓派IP>:5000`，應該會看到 "ZeroMQ Video - Raspberry Pi" 和你的鏡頭畫面
- [ ] **截圖**：瀏覽器的畫面（最好連網址列一起截），存到 `02_ZeroMQ/`
- [ ] 兩邊都按 Ctrl+C 停止程式

> PUB/SUB 不保證每一筆訊息都會送到，Subscriber 剛連上時漏掉幾張畫面是正常的。

---

## 3. Task 3：LLM 結合 WebSocket Client（port 8765）

流程：你輸入一句話 → Gemini 把它轉成 `on`、`off`、`status` 或 `unknown` → 如果不是 `unknown`，就透過 WebSocket 傳給樹莓派

**取得 Gemini API Key**
- [ ] 到 Google AI Studio → Get API key → Create API key → 複製
  > API Key 只在程式執行時貼上（程式用 `getpass` 讀取，所以輸入時畫面不會顯示）。**不要寫進程式碼、不要 commit 到 GitHub，也不要貼給 AI 或聊天工具。**

**樹莓派：啟動 Server**
```bash
cd ~/lab/MCAS-2026-IOT/Lab5/03_LLM_WebSocket
python server.py
```
（輸出跟 Task 1 一樣）

**Mac：啟動 LLM Client**
```bash
cd ~/Documents/MCAS-2026-IOT/Lab5/03_LLM_WebSocket
python client_llm.py
```
- [ ] 依序貼上 API Key（畫面上看不到）→ 輸入樹莓派 IP
- [ ] 依序測試下面幾句話：

| 輸入 | 預期的 LLM Command | 會傳給樹莓派嗎 |
|---|---|---|
| 幫我把設備打開 | `on` | ✅ |
| 可以幫我關掉嗎 | `off` | ✅ |
| 現在設備是開著還是關著？ | `status` | ✅ |
| 今天天氣如何？ | `unknown` | ❌ 會顯示「無法判斷控制指令」 |

Mac 預期輸出：
```
You: 幫我把設備打開
LLM Command: on
Server: OK: Device ON
```

- [ ] **截圖**：Mac 上的 LLM 輸出＋樹莓派 Server 的 `[RECEIVED]` 畫面（可以截兩張，或把兩個視窗並排截成一張），存到 `03_LLM_WebSocket/`

**疑難排解**
- `LLM API ERROR`：檢查 API Key 是否正確、是否超過 Rate Limit，或網路是否正常。
- `Connection failed`：樹莓派的 server.py 沒有啟動，或 IP 輸入錯誤。

---

## 4. 繳交

- [ ] 確認三個子資料夾都有放截圖
- [ ] 從 Mac push（如果截圖是在樹莓派上截的，先傳回 Mac）
  ```bash
  cd ~/Documents/MCAS-2026-IOT
  git status                      # 確認沒有 venv/ 或含 API Key 的檔案
  git add Lab5/01_WebSocket Lab5/02_ZeroMQ Lab5/03_LLM_WebSocket Lab5/Lab5_上課步驟.md
  git commit -m "Add Lab5 screenshots"
  git push origin main
  ```
- [ ] 到 Moodle 繳交 GitHub 連結：https://github.com/halipotechang/MCAS-2026-IOT/tree/main/Lab5
