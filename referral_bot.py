
import random
import string
import requests
import time
from flask import Flask
from threading import Thread

# ====== إعدادات التليجرام (قم بتعديلها) ======
TELEGRAM_BOT_TOKEN = "1737913043:AAFpsmTVhxAqx3QAMqGbC_z-hgKa-Cg1B3k"  # استبدل هذا بالتوكن الخاص ببوتك
TELEGRAM_CHAT_ID = "1058693434"          # استبدل هذا بالـ Chat ID الخاص بك
# ===========================================

# إعداد تطبيق Flask بسيط لإبقاء الخدمة نشطة على منصات مثل Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def send_telegram_message(message):
    """إرسال رسالة إلى تليجرام عند العثور على رابط."""
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def generate_referral_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_referral_link(url):
    """فحص دقيق لصلاحية الرابط."""
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        final_url = response.url
        if response.status_code != 200:
            return False
        
        # كلمات تدل على وجود عرض حقيقي
        positive_keywords = ["redeem your offer", "4 months free", "Google AI Premium", "Google One Premium"]
        page_content = response.text.lower()
        
        for keyword in positive_keywords:
            if keyword.lower() in page_content:
                return True
        return False
    except:
        return False

def main_loop():
    """الحلقة الرئيسية التي تعمل للأبد."""
    print("بدأ الفحص المستمر... سيتم إرسال تنبيه لتليجرام عند العثور على رابط.")
    while True:
        code = generate_referral_code()
        link = f"https://g.co/g1referral/{code}"
        
        if check_referral_link(link):
            msg = f"🎯 *تم العثور على رابط إحالة نشط!*\n\nالرابط: {link}\nالمالك: @H_W_O"
            print(f"وجدنا واحد! {link}")
            send_telegram_message(msg)
        
        # تأخير بسيط لتجنب الحظر من جوجل (ثانية واحدة بين كل فحص)
        time.sleep(1)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية منفصلة
    t = Thread(target=run_web)
    t.start()
    # تشغيل حلقة الفحص
    main_loop()
