# Lab6 上課步驟清單（Flask 登入 / Gemini 對話 / ngrok 公開網址）

這次的分工：**樹莓派跑 Flask 網站（port 3000）跟 ngrok，筆電和手機只用瀏覽器連進去**。

| 題目 | 配分 | 在哪裡做 | 要截圖／確認 |
|---|---|---|---|
| Lab6-1 登入／登出 | 20% | 樹莓派跑 `app.py`，筆電開瀏覽器 | 用 `admin / 1234` 登入後會進入 `/chat`，登出後會回到登入頁 |
| Lab6-2 和 Gemini 對話 | 30% | 同上 | Gemini 有回答，而且記得上一輪的內容 |
| Lab6-3 用 ngrok 從外部網路連進來 | 45% | 樹莓派開第二個終端機跑 `ngrok http 3000` | **要交的截圖**：網址列顯示 ngrok 的 HTTPS 網址，畫面上有和 Gemini 對話成功的內容 |
| 進階題 | 5% | 回家再做 | 把 Gemini 換成其他廠牌的模型 |

> ⚠️ 不要把 API Key 上傳到 GitHub（投影片寫的是扣 1000000 分）。`.env` 只放在樹莓派上，不要 commit。

Lab6 的程式重點（`app.py`）：
- 網址路徑：`/` 是登入頁，`/chat` 是聊天頁，`/api/chat` 送出問題，`/api/reset` 清除對話，`/logout` 登出
- 會從 `.env` 讀取 `GEMINI_API_KEY`、`SECRET_KEY`、`GEMINI_MODEL`
- 網站在 `0.0.0.0:3000` 上執行，`debug=False`

---

## 0. 開始前

- [ ] 確認 Lab5 已經做完（投影片 Step 19 有特別提醒）
- [x] Mac：`Lab6/` 已經在 repo 裡（`app.py`、`templates/`、`static/`、`.env.template`、`requirements.txt`）

### Step 0：樹莓派取得最新的 Lab6
保留自己改過的內容，只把助教新增的部分合併進來：
```bash
cd ~/MCAS-2026-IOT
git status                 # 先確認沒有還沒 commit 的修改
git fetch upstream
git merge upstream/main    # 如果有衝突，會停下來讓你處理，不會直接覆蓋
```
> 如果樹莓派的 repo 是從自己的 fork clone 的，而且 Mac 已經 push 過，也可以直接用 `git pull`。

### Step 1：確認 Lab6 的檔案
- [ ] 檢查檔案是否齊全
  ```bash
  cd ~/MCAS-2026-IOT/Lab6
  ls -la
  ```
  應該要看到：`app.py`、`requirements.txt`、`.env.template`、`templates/`、`static/`

---

## 1. 環境設定（樹莓派）

### Step 2：建立虛擬環境（只要做一次）
- [ ] 建立虛擬環境並安裝套件
  ```bash
  cd ~/MCAS-2026-IOT/Lab6
  python3 -m venv venv
  source venv/bin/activate
  python -m pip install -r requirements.txt
  ```
  > 會裝 `Flask==3.1.3`、`google-genai==2.28.0`、`python-dotenv==1.2.4`

### Step 3：建立 `.env`
- [ ] 複製範本
  ```bash
  cp .env.template .env
  nano .env
  ```
- [ ] 在 `GEMINI_API_KEY=` 後面貼上 API Key。可以沿用 Lab5 的 Key，沒有的話到 Google AI Studio（https://aistudio.google.com/api-keys）建立一個新的
- `GEMINI_MODEL` 保留範本的預設值就可以

### Step 4：產生 `SECRET_KEY`
- [ ] 另外開一個終端機，產生一串隨機字串
  ```bash
  python3 -c 'import secrets; print(secrets.token_hex(32))'
  ```
  > ⚠️ 投影片上的指令最後一個引號是彎引號 `’`，直接複製會出錯，要改成直引號 `'`
- [ ] 把產生的字串貼到 `.env` 的 `SECRET_KEY=` 後面
- [ ] 存檔離開：`Ctrl + O` → `Enter` → `Ctrl + X`
- `SECRET_KEY` 是 Flask 用來替 Session Cookie 簽章的金鑰

### Step 5：確認 `.env` 不會被上傳
- [ ] 檢查 `.gitignore` 和 git 狀態
  ```bash
  cd ~/MCAS-2026-IOT
  cat .gitignore      # 要有 .env 和 venv/（repo 根目錄的 .gitignore 已經有寫）
  git status          # Untracked files 裡面不應該出現 .env
  ```

---

## 2. Lab6-1、Lab6-2：在區網內測試

### Step 6：啟動 Flask（第一個終端機，啟動後不要關）
- [ ] 啟動網站
  ```bash
  cd ~/MCAS-2026-IOT/Lab6
  source venv/bin/activate     # 如果還在虛擬環境裡，可以跳過這行
  python app.py
  ```
  預期會看到 `Listening on http://0.0.0.0:3000`。出現 Development Server 的 WARNING 是正常的。

### Step 7：用筆電開啟網頁
- [ ] 查詢樹莓派的 IP：`hostname -I`
- [ ] 在筆電的瀏覽器輸入 `http://<樹莓派IP>:3000`

### Step 8：Lab6-1 登入／登出
- [ ] 帳號 `admin`、密碼 `1234` → 會進入 `/chat`
- [ ] 按右上角的「登出」→ 會回到登入頁
- （可以順便打開瀏覽器的 DevTools → Application → Cookies，看看 Flask 存的 `session` cookie。它有簽章，但沒有加密）

### Step 9：Lab6-2 測試 Gemini
- [ ] 隨便問一個問題，例如「請簡單介紹 Raspberry Pi」或「請講解傅立葉轉換」
- [ ] 接著問「請用一句話總結剛才的問題」或「我剛剛問了些什麼」，確認模型記得前面的對話

---

## 3. Lab6-3：用 ngrok 從外部網路連進來

### Step 10：在樹莓派安裝 ngrok
- [ ] 加入 ngrok 的套件來源並安裝
  ```bash
  curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
  echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" | sudo tee /etc/apt/sources.list.d/ngrok.list
  sudo apt update
  sudo apt install ngrok
  ```

### Step 11：設定 ngrok 帳號
- [ ] 到 ngrok Dashboard 註冊帳號，在「Your Authtoken」頁面複製 Token
- [ ] 在樹莓派上設定 Token
  ```bash
  ngrok config add-authtoken <你的Token>
  ```
  > Authtoken 也是機密資料，不要放進 repo，也不要截圖

### Step 12：開第二個終端機，建立公開網址
- [ ] 第一個終端機的 Flask 保持執行
- [ ] 在新的終端機執行
  ```bash
  ngrok http 3000
  ```
  畫面上 `Forwarding` 那一行會出現類似 `https://xxxxx.ngrok.app` 的網址

### Step 13：從外部網路測試
- [ ] 手機關掉 Wi-Fi，改用 4G/5G（重點是不要和樹莓派在同一個網路）
- [ ] 打開 ngrok 給的 HTTPS 網址，用 `admin / 1234` 登入，進入 `/chat`
- [ ] 和 Gemini 完成至少一輪對話

### Step 14：截圖交作業
- [ ] 截圖要**同時**拍到：
  1. 網址列顯示 ngrok 的公開 HTTPS 網址
  2. 網頁上和 Gemini 對話成功的內容
- [ ] 截圖存到 `Lab6/` 資料夾，然後 commit 並 push（**`.env` 不能 commit**）
- [ ] 做完以後，在 ngrok 的終端機按 `Ctrl + C` 關閉 Tunnel；Flask 也按 `Ctrl + C` 停止

---

## 常見問題

| 狀況 | 檢查哪裡 |
|---|---|
| 一啟動就報錯，說缺少 KEY | `.env` 是不是放在 `Lab6/` 裡面、`GEMINI_API_KEY` 和 `SECRET_KEY` 有沒有填 |
| 筆電連不上 `:3000` | 兩台是不是在同一個網路、IP 有沒有打對、Flask 是不是還在執行 |
| Gemini 沒有回應 | API Key 是否有效、`GEMINI_MODEL` 名稱是否正確、樹莓派能不能連上網路 |
| ngrok 顯示 `authentication failed` | 重新執行 Step 11 的 `add-authtoken` |
| ngrok 網址打不開 | Flask 有沒有關掉、ngrok 指令的 port 是不是 `3000` |
