import os
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8696673043:AAFH0FgQG5UhS7x2iH_AdEgqCk2VgkuJoP4')
app = Flask(__name__)

def get_bot_response(message):
    text = message.lower()
    
    if any(word in text for word in ['start', '/start', 'مرحب', 'هلا', 'السلام']):
        return """أهلاً وسهلاً! 👋

🏢 شركة جزء بالمية للتطوير والاستثمار العقاري

📊 استثمر معنا:
- 3 عقارات تجارية بالرياض
- قيمة المحفظة: 9 مليون ريال
- عوائد سنوية: 8.44% - 10.16%
- بداية من 1,000 ريال
- توزيع عوائد ربع سنوي

📞 للتواصل:
- الجوال: 0593064061
- البريد: info@juzabilmia.com
- الموقع: juzabilmia.com"""
    
    elif any(word in text for word in ['كم', 'مبلغ', 'استثمار', 'سعر']):
        return "💰 بداية من 1000 ريال\n📈 عوائد 8.44% - 10.16% سنوياً\n🔄 توزيع أرباح ربع سنوي\n\nللتفاصيل: 0593064061"
    
    elif any(word in text for word in ['تواصل', 'رقم', 'هاتف']):
        return "📞 0593064061\n📧 info@juzabilmia.com\n🌐 juzabilmia.com"
    
    else:
        return "شكراً لاهتمامك! 🙏\nجزء بالمية - استثمار عقاري ذكي\nللاستفسار: 0593064061"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        response = get_bot_response(text)
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", {
            'chat_id': chat_id, 'text': response
        })
    return "OK"

@app.route('/')
def home():
    return "🤖 Juz Bilmia Bot - جاهز ويعمل!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
