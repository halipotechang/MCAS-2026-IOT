"""
Lab6 進階題：把 Gemini 換成 DeepSeek

和原本 Lab6/app.py 的差異：
- DeepSeek 提供 OpenAI 相容的 API，所以用 openai SDK，把 base_url 指到 DeepSeek
- Gemini 的 Interactions API 會在伺服器端記住對話（previous_interaction_id），
  DeepSeek 的 /chat/completions 是 stateless，每次都要把完整對話紀錄送過去，
  所以這裡在 Flask 伺服器的記憶體裡保存每個登入者的對話紀錄。
"""

import os
import uuid
from functools import wraps

import openai
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from openai import OpenAI


# =========================
# Environment Variables
# =========================

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")

if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "YOUR_API_KEY_HERE":
    raise RuntimeError(
        "找不到 DEEPSEEK_API_KEY，請先在 .env 填入 API Key。"
    )

if not SECRET_KEY or SECRET_KEY == "CHANGE_ME":
    raise RuntimeError("請在 .env 設定安全的 SECRET_KEY。")


# =========================
# Flask
# =========================

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Lab 用簡化帳號
# 正式系統不應以明文保存密碼
USERS = {
    "admin": "1234",
}


# =========================
# DeepSeek
# =========================

deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

SYSTEM_PROMPT = "你是 IoT 課程的助教，請用繁體中文回答，回答盡量簡潔。"

# 對話紀錄存在伺服器記憶體：{conversation_id: [messages...]}
# Flask session cookie 只有約 4KB，放不下完整對話，所以 cookie 裡只存 conversation_id。
# 伺服器重開後紀錄會消失，Lab 用途足夠。
CONVERSATIONS = {}


def ask_deepseek(conversation_id, message):
    history = CONVERSATIONS.setdefault(conversation_id, [])

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": message}]
    )

    response = deepseek_client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        # 聊天不需要深度推理，關掉 thinking 模式，回應比較快
        extra_body={"thinking": {"type": "disabled"}},
    )

    reply = (response.choices[0].message.content or "").strip()

    if not reply:
        return "DeepSeek 沒有回傳文字內容。"

    # 成功才寫入對話紀錄，下一輪把整段送回去，模型才記得前面的內容
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    return reply


# =========================
# Login Required
# =========================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user" not in session:

            # API 不做 redirect
            if request.path.startswith("/api/"):
                return jsonify({"error": "請先登入"}), 401

            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


# =========================
# Login
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username in USERS and USERS[username] == password:
            session.clear()
            session["user"] = username
            session["conversation_id"] = uuid.uuid4().hex
            return redirect(url_for("chat_room"))

        return render_template("login.html", msg="帳號或密碼錯誤")

    if "user" in session:
        return redirect(url_for("chat_room"))

    return render_template("login.html")


# =========================
# Chat Page
# =========================

@app.get("/chat")
@login_required
def chat_room():
    return render_template("chat.html", username=session["user"])


# =========================
# DeepSeek API
# =========================

@app.post("/api/chat")
@login_required
def api_chat():

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "訊息不可為空"}), 400

    if len(message) > 2000:
        return jsonify({"error": "訊息過長"}), 400

    conversation_id = session.setdefault("conversation_id", uuid.uuid4().hex)

    try:
        reply = ask_deepseek(conversation_id, message)
        return jsonify({"reply": reply})

    except openai.AuthenticationError:
        print("[DeepSeek API Error] API Key 無效")
        return jsonify({"error": "DeepSeek API Key 無效，請檢查 .env。"}), 502

    except openai.RateLimitError:
        print("[DeepSeek API Error] 超過速率限制或額度不足")
        return jsonify({"error": "DeepSeek API 呼叫太頻繁或額度不足，請稍後再試。"}), 502

    except openai.APIStatusError as error:
        print("[DeepSeek API Error]", error.status_code, error.message)
        return jsonify({"error": "DeepSeek API 呼叫失敗，請檢查模型設定或帳戶餘額。"}), 502

    except openai.APIConnectionError as error:
        print("[DeepSeek API Error] 連線失敗", error)
        return jsonify({"error": "無法連線到 DeepSeek API，請檢查網路。"}), 502


# =========================
# Reset Conversation
# =========================

@app.post("/api/reset")
@login_required
def reset_chat():
    CONVERSATIONS.pop(session.get("conversation_id"), None)
    session["conversation_id"] = uuid.uuid4().hex
    return jsonify({"ok": True})


# =========================
# Logout
# =========================

@app.post("/logout")
@login_required
def logout():
    CONVERSATIONS.pop(session.get("conversation_id"), None)
    session.clear()
    return redirect(url_for("login"))


# =========================
# Run Server
# =========================

if __name__ == "__main__":

    print("=== Lab6 Advanced: Flask + DeepSeek ===")
    print(f"Model: {DEEPSEEK_MODEL}")
    print("Listening on http://0.0.0.0:3000")
    print("Debug mode is OFF")

    app.run(host="0.0.0.0", port=3000, debug=False)
