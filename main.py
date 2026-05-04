import os
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
app = Flask(__name__)

# ========== لغة المستخدم (في الذاكرة) ==========
user_lang = {}

def L(chat_id):
    return user_lang.get(chat_id, 'ar')

# ========== القائمة الرئيسية ==========
def main_menu(chat_id):
    lang = L(chat_id)
    if lang == 'ar':
        return {
            'inline_keyboard': [
                [{'text': '🏢 عن الشركة', 'callback_data': 'about'},
                 {'text': '💎 كيف نعمل', 'callback_data': 'how'}],
                [{'text': '📊 المحفظة العقارية', 'callback_data': 'portfolio'},
                 {'text': '🧮 حاسبة الاستثمار', 'callback_data': 'calc'}],
                [{'text': '⭐ مميزاتنا', 'callback_data': 'features'},
                 {'text': '⚖️ الرقابة الشرعية', 'callback_data': 'sharia'}],
                [{'text': '📜 التراخيص', 'callback_data': 'licenses'},
                 {'text': '❓ الأسئلة الشائعة', 'callback_data': 'faq'}],
                [{'text': '💳 الدفع الآمن', 'callback_data': 'payment'},
                 {'text': '📱 التطبيق', 'callback_data': 'app'}],
                [{'text': '✍️ سجّل الآن', 'url': 'https://juzabilmia.com/register.html'}],
                [{'text': '📧 البريد الرسمي', 'url': 'mailto:info@juzabilmia.com'},
                 {'text': '🌐 الموقع', 'url': 'https://juzabilmia.com'}],
                [{'text': '🇬🇧 English', 'callback_data': 'lang_en'}]
            ]
        }
    else:
        return {
            'inline_keyboard': [
                [{'text': '🏢 About Us', 'callback_data': 'about'},
                 {'text': '💎 How It Works', 'callback_data': 'how'}],
                [{'text': '📊 Portfolio', 'callback_data': 'portfolio'},
                 {'text': '🧮 Calculator', 'callback_data': 'calc'}],
                [{'text': '⭐ Features', 'callback_data': 'features'},
                 {'text': '⚖️ Sharia Compliance', 'callback_data': 'sharia'}],
                [{'text': '📜 Licenses', 'callback_data': 'licenses'},
                 {'text': '❓ FAQ', 'callback_data': 'faq'}],
                [{'text': '💳 Secure Payment', 'callback_data': 'payment'},
                 {'text': '📱 Mobile App', 'callback_data': 'app'}],
                [{'text': '✍️ Register Now', 'url': 'https://juzabilmia.com/register.html'}],
                [{'text': '📧 Official Email', 'url': 'mailto:info@juzabilmia.com'},
                 {'text': '🌐 Website', 'url': 'https://juzabilmia.com'}],
                [{'text': '🇸🇦 العربية', 'callback_data': 'lang_ar'}]
            ]
        }

# ========== زر العودة ==========
def back_btn(chat_id):
    lang = L(chat_id)
    txt = '🔙 القائمة الرئيسية' if lang == 'ar' else '🔙 Main Menu'
    return {'inline_keyboard': [[{'text': txt, 'callback_data': 'menu'}]]}

# ========== نصوص العربية ==========
TEXTS_AR = {
    'welcome': """🌟 *أهلاً بك في شركة جزء بالمية*

🏢 *التملك العقاري الجزئي في المملكة*

عرض عقارات تجارية وسكنية مؤجرة مسبقاً
بحد أدنى *1,000 ريال* للحصة
عوائد تقديرية تصل إلى *10.16% سنوياً* (بعد الترخيص)

⚠️ *نحن في مرحلة إطلاق تجريبي ومقدّمون على البيئة التنظيمية التجريبية لهيئة العقار، ولم يصدر لنا ترخيص بمزاولة نشاط التملك العقاري الجزئي بعد. لا يتم حالياً بيع حصص أو تحصيل مبالغ.*

👇 *اختر ما تريد معرفته:*""",

    'about': """🏢 *عن شركة جزء بالمية*

*شركة جزء بالمية للتطوير والاستثمار العقاري*
شركة سعودية متخصصة في التملك العقاري الجزئي

📍 *المقر:* الرياض، المملكة العربية السعودية
🏛️ *السجل التجاري:* 7040575412
💼 *رأس المال:* 100,000 ريال

🎯 *رؤيتنا:*
وفقاً للخطة المعتمدة بعد صدور الترخيص، نتيح لك تملك حصة في عقارات تجارية وسكنية مؤجرة بعقود سارية، والحصول على عوائد إيجارية ربع سنوية، بمبلغ يبدأ من 1,000 ريال للحصة.

✅ بدون تعقيدات
✅ بدون وسطاء
✅ بدون حد أدنى مرتفع

📞 *تواصل:*
- البريد: info@juzabilmia.com
- الموقع: juzabilmia.com""",

    'how': """💎 *كيف تعمل جزء بالمية؟*

*4 خطوات وأنت مستثمر عقاري:*

1️⃣ *سجّل مجاناً*
أنشئ حسابك في دقيقتين وتحقق من هويتك بشكل آمن

2️⃣ *اختر عقارك*
تصفح 3 عقارات تجارية وسكنية مؤجرة مسبقاً في الرياض

3️⃣ *اشترِ حصتك*
استثمر من 1,000 ريال وامتلك حصة موثقة رسمياً

4️⃣ *احصل على عائدك*
عائد إيجاري منتظم يُوزَّع *ربع سنوياً*

🔒 *جميع العقود موثقة في:*
- منصة إيجار الحكومية
- هيئة العقار (REGA)
- البنك المركزي (ساما) عبر ميسّر""",

    'portfolio': """📊 *المحفظة العقارية*

*3 عقارات تجارية وسكنية في الرياض — مؤجرة بعقود رسمية*

━━━━━━━━━━━━━━━

🏢 *العقار الأول*
📍 الرياض، عقار مؤجر
💰 القيمة: 3.5 مليون ريال
📈 العائد السنوي: 6.71%
📊 الحصص: 3,500 حصة
✅ مقيّم معتمد | مفتوح للاستثمار

━━━━━━━━━━━━━━━

🏢 *العقار الثاني — الأعلى عائداً ⭐*
📍 الرياض، عقار مؤجر
💰 القيمة: 3 مليون ريال
📈 العائد السنوي: *10.16%*
📊 الحصص: 3,000 حصة
✅ مقيّم معتمد

━━━━━━━━━━━━━━━

🏢 *العقار الثالث*
📍 الرياض، عقار مؤجر
💰 القيمة: 2.5 مليون ريال
📈 العائد السنوي: 8.8%
📊 الحصص: 2,500 حصة
✅ مقيّم معتمد | مفتوح

━━━━━━━━━━━━━━━

📈 *إجمالي المحفظة:*
- 9,000,000 ريال
- 9,000 حصة متاحة
- متوسط العائد: *8.44%*
- إيجارات سنوية: 759,750 ريال""",

    'features': """⭐ *لماذا جزء بالمية الخيار الأفضل؟*

✅ *متوافق مع الشريعة الإسلامية*
عقود تملك حقيقي وتأجير متوافقة مع أحكام الشريعة

✅ *آلية تخارج واضحة*
بيع الحصة بعد سنة من التملك بكل سهولة

✅ *بيع العقار بعد 3-5 سنوات*
أو عند ارتفاع قيمته 30%، مع توزيع العوائد طوال المدة

✅ *حد منخفض للاستثمار*
ابدأ بـ 1,000 ريال فقط للحصة الواحدة

✅ *تقييم عقاري معتمد*
من مقيّمين معتمدين لدى هيئة العقار

✅ *عقود موثقة إلكترونياً*
في منصة إيجار الحكومية

✅ *مساعد ذكي 24/7*
بوت تيليجرام (وأنت معه الآن! 😊)""",

    'sharia': """⚖️ *الرقابة الشرعية والقانونية*

*نموذج شرعي وقانوني متكامل*

━━━━━━━━━━━━━━━

✅ *اللجنة الشرعية*
نموذج الشركة حاصل على مراجعة شرعية معتمدة تضمن توافق جميع العمليات مع أحكام الشريعة الإسلامية في التملك العقاري الجزئي.

━━━━━━━━━━━━━━━

✅ *المراجعة القانونية*
جميع العقود والاتفاقيات مُراجَعة ومعتمدة قانونياً من متخصصين، وموثقة وفق أحكام الأنظمة والتشريعات السعودية.

━━━━━━━━━━━━━━━

✅ *البيئة التنظيمية التجريبية*
تم تقديم الطلب للانضمام إلى البيئة التنظيمية التجريبية للعمل تحت إشراف تنظيمي مباشر من الهيئة العامة للعقار.

━━━━━━━━━━━━━━━

🛡️ *التزامنا:*
- لا استثمار في أنشطة محرَّمة
- لا ضمان مخالف للشريعة
- شفافية كاملة في جميع العمليات""",

    'licenses': """📜 *الوثائق والتراخيص الرسمية*

*التراخيص والوثائق الرسمية الحالية*

━━━━━━━━━━━━━━━

📄 *رخصة فال للوساطة والتسويق*
رقم: 1200027650
سارية حتى: 23/06/2027

📄 *رخصة فال لإدارة الأملاك*
رقم: 2200003901
سارية حتى: 23/06/2027

📄 *السجل التجاري*
رقم: 7040575412

📄 *عضوية الغرفة التجارية*
رقم: 965892

📄 *شهادة معروف*
رقم: 372715

📄 *عضوية إيجار*
EJAR_86992343

📄 *ترخيص ميسّر المالية*
من البنك المركزي السعودي (ساما)
رقم: 16/م ش م/1443

━━━━━━━━━━━━━━━

✅ جميع التراخيص صادرة من الجهات الحكومية المختصة""",

    'payment': """💳 *الدفع الآمن*

*بوابة ميسّر المالية (Moyasar)*

🏛️ مُرخّصة من *البنك المركزي السعودي (ساما)*
🛡️ متوافقة مع معيار الأمان الدولي *PCI-DSS*

━━━━━━━━━━━━━━━

🔐 *الحماية:*
- جميع المعاملات مُشفّرة عبر SSL/TLS
- لا يتم تخزين بيانات بطاقتك على خوادمنا
- حماية كاملة من Cloudflare WAF + DDoS

━━━━━━━━━━━━━━━

💳 *وسائل الدفع المدعومة:*
✅ مدى
✅ Visa
✅ Mastercard
✅ Apple Pay

━━━━━━━━━━━━━━━

🔒 *معايير الأمان:*
- SSL/TLS Full Strict Encryption
- Honeypot نشط — حماية من البوتات الضارة
- TLS 1.2/1.3 أحدث معايير التشفير""",

    'app': """📱 *تطبيق جزء بالمية*

استثمر وتابع محفظتك العقارية من هاتفك في أي وقت

📲 *قريباً جداً على:*
- App Store (iOS)
- Google Play (Android)

━━━━━━━━━━━━━━━

✨ *مميزات التطبيق:*
- تصفح العقارات المتاحة
- شراء حصص فوري
- تتبع العائد الربع سنوي
- محفظة استثمارية شاملة
- إشعارات فورية

🎯 سجّل اهتمامك الآن لتكون من *أوائل المستخدمين*

🌐 juzabilmia.com""",

    'faq': """❓ *الأسئلة الشائعة*

اختر السؤال:""",

    'calc': """🧮 *حاسبة العائد*

*أمثلة سريعة على العائد المتوقع:*

━━━━━━━━━━━━━━━

💰 *استثمار 1,000 ريال*
- عائد سنوي 8.44%: 84 ريال/سنة
- ربع سنوي: 21 ريال
- صافي بعد الرسوم (10%): 76 ريال

━━━━━━━━━━━━━━━

💰 *استثمار 10,000 ريال*
- عائد سنوي 8.44%: 844 ريال/سنة
- ربع سنوي: 211 ريال
- صافي بعد الرسوم: 760 ريال

━━━━━━━━━━━━━━━

💰 *استثمار 50,000 ريال*
- عائد سنوي 10.16%: 5,080 ريال/سنة
- ربع سنوي: 1,270 ريال
- صافي بعد الرسوم: 4,572 ريال

━━━━━━━━━━━━━━━

💰 *استثمار 100,000 ريال*
- عائد سنوي 10.16%: 10,160 ريال/سنة
- ربع سنوي: 2,540 ريال
- صافي بعد الرسوم: 9,144 ريال

━━━━━━━━━━━━━━━

📊 *ملاحظات:*
- الرسوم: 5% إدارة + 5% صيانة = 10%
- التوزيع: ربع سنوي
- المدة: 3-5 سنوات

🌐 لحاسبة تفاعلية:
juzabilmia.com""",

    'platform_correction': """📍 *تصحيح مهم:*

*جزء بالمية* ليست منصة — بل هي *شركة سعودية موثقة رسمياً* (السجل التجاري والرخص أدناه).

🏢 *الاسم الكامل:*
شركة جزء بالمية للتطوير والاستثمار العقاري

🏛️ *السجل التجاري:* 7040575412
📄 *رخصة فال للوساطة:* 1200027650
📄 *رخصة إدارة الأملاك:* 2200003901
📄 *عضوية الغرفة التجارية:* 965892

✅ موثقون رسمياً (سجل تجاري + رخص فال + معروف)
✅ مقدّمون على البيئة التنظيمية التجريبية لهيئة العقار
✅ نموذج متوافق مع الشريعة الإسلامية

اطلع على المزيد من القائمة 👇"""
}

# ========== أسئلة شائعة ==========
def faq_menu(chat_id):
    lang = L(chat_id)
    if lang == 'ar':
        return {
            'inline_keyboard': [
                [{'text': '1️⃣ ما هو التملك الجزئي؟', 'callback_data': 'q1'}],
                [{'text': '2️⃣ هل العقارات موجودة فعلياً؟', 'callback_data': 'q2'}],
                [{'text': '3️⃣ كم العائد السنوي؟', 'callback_data': 'q3'}],
                [{'text': '4️⃣ هل الشركة مرخصة؟', 'callback_data': 'q4'}],
                [{'text': '5️⃣ كيف أتواصل معكم؟', 'callback_data': 'q5'}],
                [{'text': '6️⃣ ما هي رسوم الإدارة؟', 'callback_data': 'q6'}],
                [{'text': '7️⃣ كيف أبيع حصتي؟', 'callback_data': 'q7'}],
                [{'text': '8️⃣ العائد صافٍ أم إجمالي؟', 'callback_data': 'q8'}],
                [{'text': '9️⃣ ما الحد الأدنى؟', 'callback_data': 'q9'}],
                [{'text': '🔟 ماذا عن الضريبة؟', 'callback_data': 'q10'}],
                [{'text': '1️⃣1️⃣ من يتحمل الصيانة؟', 'callback_data': 'q11'}],
                [{'text': '1️⃣2️⃣ هل الدفع آمن؟', 'callback_data': 'q12'}],
                [{'text': '🔙 القائمة الرئيسية', 'callback_data': 'menu'}]
            ]
        }
    else:
        return {
            'inline_keyboard': [
                [{'text': '1️⃣ What is fractional ownership?', 'callback_data': 'q1'}],
                [{'text': '2️⃣ Are properties real?', 'callback_data': 'q2'}],
                [{'text': '3️⃣ Annual return?', 'callback_data': 'q3'}],
                [{'text': '4️⃣ Licensed company?', 'callback_data': 'q4'}],
                [{'text': '5️⃣ How to contact?', 'callback_data': 'q5'}],
                [{'text': '6️⃣ Management fees?', 'callback_data': 'q6'}],
                [{'text': '7️⃣ How to sell shares?', 'callback_data': 'q7'}],
                [{'text': '8️⃣ Net or gross return?', 'callback_data': 'q8'}],
                [{'text': '9️⃣ Minimum investment?', 'callback_data': 'q9'}],
                [{'text': '🔟 Tax info?', 'callback_data': 'q10'}],
                [{'text': '1️⃣1️⃣ Maintenance costs?', 'callback_data': 'q11'}],
                [{'text': '1️⃣2️⃣ Is payment secure?', 'callback_data': 'q12'}],
                [{'text': '🔙 Main Menu', 'callback_data': 'menu'}]
            ]
        }

FAQ_AR = {
    'q1': """*١. ما هو التملك العقاري الجزئي؟*

نموذج يتيح لك تملك حصة في عقار تجاري أو سكني بمبلغ يبدأ من *1,000 ريال* والحصول على نصيبك من عوائد الإيجار بنسبة حصتك.

✅ تملك موثق رسمياً
✅ عوائد إيجارية ربع سنوية
✅ شفافية كاملة""",

    'q2': """*٢. هل العقارات موجودة فعلياً؟*

نعم، لدينا *3 عقارات تجارية وسكنية بقيمة 9 مليون ريال* محددة في الرياض، جميعها مؤجرة مسبقاً بعقود سارية عبر شبكة إيجار.

🏢 الشركة تعمل على الاستحواذ عليها ونقل ملكيتها للمستثمرين عبر آلية التملك الجزئي بعد صدور الترخيص الرسمي من الهيئة العامة للعقار.""",

    'q3': """*٣. كم يبلغ العائد السنوي؟*

📈 يتراوح بين *6.71% و10.16%*
📊 بمتوسط *8.44% سنوياً*

ملاحظة: جميع النسب المعروضة هي *عوائد إجمالية* قبل خصم رسوم الإدارة.

🔄 يُوزَّع العائد *ربع سنوياً* إلى حساب المستثمر.""",

    'q4': """*٤. هل الشركة مرخصة؟*

الشركة حاصلة على:
📄 *رخصة فال للوساطة:* 1200027650
📄 *رخصة إدارة الأملاك:* 2200003901
📄 *عضوية إيجار وغرفة تجارية وشهادة معروف*

⚠️ *وضعنا التنظيمي:* مقدّمون على البيئة التنظيمية التجريبية للهيئة العامة للعقار (REGA)، *ولم يصدر لنا حتى تاريخه ترخيص بمزاولة نشاط التملك العقاري الجزئي*.

📌 لن يبدأ النشاط الفعلي (بيع الحصص، تحصيل المبالغ، نقل الملكيات، توزيع العوائد) إلا بعد صدور الترخيص الرسمي.""",

    'q5': """*٥. كيف أتواصل معكم؟*

📧 *البريد الرسمي:* info@juzabilmia.com
🤖 *تيليجرام:* @JuzBilmia2026_bot
🌐 *الموقع:* juzabilmia.com

⏰ متاحون 24/7 عبر البوت
🕒 الإدارة: الأحد - الخميس، 9ص - 6م""",

    'q6': """*٦. ما هي رسوم الإدارة السنوية؟*

💼 *رسوم الإدارة:* 5% من الإيجار السنوي المحصّل
🔧 *صندوق الصيانة:* 5% من الإيجار الإجمالي

━━━━━━━━━━━━━━━

📊 *إجمالي الاستقطاعات: 10% من الإيجار*
(5% إدارة + 5% صيانة)

ملاحظة: هذه المصاريف منفصلة عن بعضها — صندوق الصيانة لتغطية مصاريف العقار، ولا يدخل ضمن رسوم الإدارة.""",

    'q7': """*٧. كيف يمكنني بيع حصتي (التخارج)؟*

⏳ بعد *سنة* من التملك يمكنك طلب بيع حصتك عبر الخدمة.

💰 *عمولة التخارج:* 1% من قيمة الصفقة عند إتمام البيع
📅 *مدة النقل:* خلال 14 يوم عمل

✅ آلية تخارج واضحة وشفافة""",

    'q8': """*٨. هل العائد المعروض صافٍ أم إجمالي؟*

العائد المعروض *إجمالي*.

📊 *العائد الصافي* = العائد الإجمالي ناقص:
- رسوم الإدارة (5%)
- صندوق الصيانة (5%)
= خصم 10% من الإيجار

━━━━━━━━━━━━━━━

📌 *مثال:*
عائد 10.16% إجمالي ≈ *9.14% صافٍ*

🔄 يُوزَّع العائد *ربع سنوياً* إلى حساب المستثمر.""",

    'q9': """*٩. ما هو الحد الأدنى للاستثمار؟*

💰 *الحد الأدنى: 1,000 ريال*
(سعر الوحدة الواحدة)

✅ يمكنك شراء أي عدد من الوحدات بحسب ميزانيتك
✅ مناسب لشريحة واسعة من المستثمرين""",

    'q10': """*١٠. ما موقف الضريبة على عوائد الاستثمار؟*

الشركة *مسجلة رسمياً في ضريبة القيمة المضافة* لدى هيئة الزكاة والضريبة والجمارك.

🧾 *الرقم الضريبي:* 314770310200003
📅 *نفاذ التسجيل:* 01/06/2026

📊 تُطبّق ضريبة 15% على *رسوم الإدارة فقط* وفقاً للمادة (36) من اللائحة التنفيذية. قيمة الحصة الأساسية (1,000 ريال) معفاة كمعاملة استثمارية.

📧 للتفاصيل: *info@juzabilmia.com*""",

    'q11': """*١١. من يتحمل مصاريف الصيانة؟*

🛡️ مصاريف الصيانة *مغطاة بالكامل* من صندوق الصيانة

📊 *5%* تُستقطع تلقائياً من الإيجار المحصَّل

✅ *لا يُطالَب المستثمر بأي مبالغ إضافية*""",

    'q12': """*١٢. هل عملية الدفع آمنة؟*

نعم، نعتمد على بوابة *ميسّر المالية (Moyasar)*:

🏛️ مُرخّصة من *البنك المركزي السعودي (ساما)*
🛡️ متوافقة مع معيار *PCI-DSS* الدولي

🔐 *الحماية:*
- تشفير SSL/TLS لكل المعاملات
- لا تخزين لبيانات البطاقة (CVV/الرقم/الانتهاء)

💳 *وسائل الدفع:*
✅ مدى | Visa | Mastercard | Apple Pay"""
}

# ========== نصوص الإنجليزية ==========
TEXTS_EN = {
    'welcome': """🌟 *Welcome to Juz Bilmia*

🏢 *Fractional Real Estate Ownership in KSA*

Showcasing pre-leased commercial and residential properties
Minimum *SAR 1,000* per share
Estimated returns up to *10.16% annually* (post-license)

⚠️ *We are in a pilot phase and have applied to REGA's regulatory sandbox. We have NOT yet been granted a license to operate fractional real estate activities. No share sales, fund collection, ownership transfers, or distributions are taking place at this time.*

👇 *Choose what you'd like to know:*""",

    'about': """🏢 *About Juz Bilmia Company*

*Juz Bilmia Real Estate Development & Investment*
A Saudi company specialized in fractional property ownership

📍 *HQ:* Riyadh, Saudi Arabia
🏛️ *Commercial Registration:* 7040575412
💼 *Capital:* SAR 100,000

🎯 *Our Vision:*
Per our approved plan post-license, enable you to own a share in pre-leased commercial and residential properties and earn quarterly rental returns, starting from SAR 1,000 per share.

✅ No complications
✅ No middlemen
✅ No high minimums

📞 *Contact:*
- Email: info@juzabilmia.com
- Web: juzabilmia.com""",

    'how': """💎 *How Does Juz Bilmia Work?*

*4 steps to become a real estate investor:*

1️⃣ *Register for Free*
Create your account in 2 minutes with secure KYC

2️⃣ *Choose Your Property*
Browse 3 pre-leased commercial and residential properties in Riyadh

3️⃣ *Buy Your Share*
Invest from SAR 1,000 and own a documented share

4️⃣ *Receive Returns*
Regular rental income distributed *quarterly*

🔒 *All contracts documented at:*
- Ejar Government Platform
- REGA Authority
- Central Bank (SAMA) via Moyasar""",

    'portfolio': """📊 *Real Estate Portfolio*

*3 Commercial and Residential Properties in Riyadh — Officially Leased*

━━━━━━━━━━━━━━━

🏢 *Property 1*
📍 Riyadh, Officially Leased
💰 Value: SAR 3.5M
📈 Annual Return: 6.71%
📊 Shares: 3,500
✅ Certified Valuation

━━━━━━━━━━━━━━━

🏢 *Property 2 — Highest Return ⭐*
📍 Riyadh, Officially Leased
💰 Value: SAR 3M
📈 Annual Return: *10.16%*
📊 Shares: 3,000
✅ Certified Valuation

━━━━━━━━━━━━━━━

🏢 *Property 3*
📍 Riyadh, Officially Leased
💰 Value: SAR 2.5M
📈 Annual Return: 8.8%
📊 Shares: 2,500
✅ Certified Valuation

━━━━━━━━━━━━━━━

📈 *Total Portfolio:*
- SAR 9,000,000
- 9,000 shares available
- Average return: *8.44%*
- Annual rentals: SAR 759,750""",

    'features': """⭐ *Why Choose Juz Bilmia?*

✅ *Sharia-Compliant*
Real ownership and leasing contracts compliant with Islamic law

✅ *Clear Exit Mechanism*
Sell your share after 1 year easily

✅ *Property Sale in 3-5 Years*
Or when value rises by 30%, with returns throughout

✅ *Low Entry Threshold*
Start with just SAR 1,000 per share

✅ *Certified Valuations*
By REGA-certified valuers via Taqeem platform

✅ *Electronically Documented Contracts*
On Ejar government platform

✅ *24/7 AI Assistant*
Telegram bot (you're using it now! 😊)""",

    'sharia': """⚖️ *Sharia & Legal Compliance*

*Complete Sharia and Legal Framework*

━━━━━━━━━━━━━━━

✅ *Sharia Committee*
The company model has approved Sharia review ensuring compliance with Islamic law in fractional real estate ownership.

━━━━━━━━━━━━━━━

✅ *Legal Review*
All contracts reviewed and legally approved by specialists, documented per Saudi laws.

━━━━━━━━━━━━━━━

✅ *Regulatory Sandbox*
Application submitted to join REGA's regulatory sandbox under direct regulatory supervision.

━━━━━━━━━━━━━━━

🛡️ *Our Commitment:*
- No investment in prohibited activities
- No Sharia-violating guarantees
- Full transparency in all operations""",

    'licenses': """📜 *Official Licenses*

*Current Licenses and Official Documents*

━━━━━━━━━━━━━━━

📄 *FAL Brokerage License*
No: 1200027650
Valid until: 23/06/2027

📄 *FAL Property Management License*
No: 2200003901
Valid until: 23/06/2027

📄 *Commercial Registration*
No: 7040575412

📄 *Chamber of Commerce*
No: 965892

📄 *Maroof Certificate*
No: 372715

📄 *Ejar Membership*
EJAR_86992343

📄 *Moyasar License*
From SAMA (Central Bank)
No: 16/م ش م/1443

━━━━━━━━━━━━━━━

✅ All licenses issued by official Saudi authorities""",

    'payment': """💳 *Secure Payment*

*Moyasar Financial Gateway*

🏛️ Licensed by *SAMA (Saudi Central Bank)*
🛡️ *PCI-DSS* compliant

━━━━━━━━━━━━━━━

🔐 *Security:*
- All transactions encrypted via SSL/TLS
- No card data stored on our servers
- Cloudflare WAF + DDoS protection

━━━━━━━━━━━━━━━

💳 *Supported Methods:*
✅ Mada
✅ Visa
✅ Mastercard
✅ Apple Pay

━━━━━━━━━━━━━━━

🔒 *Security Standards:*
- SSL/TLS Full Strict Encryption
- Active Honeypot — bot protection
- TLS 1.2/1.3 latest encryption""",

    'app': """📱 *Juz Bilmia App*

Invest and track your portfolio anytime

📲 *Coming Soon on:*
- App Store (iOS)
- Google Play (Android)

━━━━━━━━━━━━━━━

✨ *App Features:*
- Browse available properties
- Instant share purchase
- Track quarterly returns
- Comprehensive portfolio
- Real-time notifications

🎯 Register interest now to be among *first users*

🌐 juzabilmia.com""",

    'faq': """❓ *Frequently Asked Questions*

Choose a question:""",

    'calc': """🧮 *Return Calculator*

*Quick examples of expected returns:*

━━━━━━━━━━━━━━━

💰 *SAR 1,000 investment*
- Annual return 8.44%: SAR 84/year
- Quarterly: SAR 21
- Net after fees (10%): SAR 76

━━━━━━━━━━━━━━━

💰 *SAR 10,000 investment*
- Annual return 8.44%: SAR 844/year
- Quarterly: SAR 211
- Net after fees: SAR 760

━━━━━━━━━━━━━━━

💰 *SAR 50,000 investment*
- Annual return 10.16%: SAR 5,080/year
- Quarterly: SAR 1,270
- Net after fees: SAR 4,572

━━━━━━━━━━━━━━━

💰 *SAR 100,000 investment*
- Annual return 10.16%: SAR 10,160/year
- Quarterly: SAR 2,540
- Net after fees: SAR 9,144

━━━━━━━━━━━━━━━

📊 *Notes:*
- Fees: 5% management + 5% maintenance = 10%
- Distribution: Quarterly
- Duration: 3-5 years

🌐 Interactive calculator:
juzabilmia.com""",

    'platform_correction': """📍 *Important Clarification:*

*Juz Bilmia* is not a platform — it is an *officially registered Saudi company* (CR and FAL licenses below).

🏢 *Full Name:*
Juz Bilmia Real Estate Development & Investment

🏛️ *Commercial Registration:* 7040575412
📄 *FAL Brokerage License:* 1200027650
📄 *Property Management License:* 2200003901
📄 *Chamber of Commerce:* 965892

✅ Officially documented (CR + FAL Licenses + Maroof)
✅ Applicant in REGA's regulatory sandbox program
✅ Sharia-compliant model

Explore more from the menu 👇"""
}

FAQ_EN = {
    'q1': """*1. What is fractional real estate ownership?*

A model that allows you to own a share in a commercial or residential property starting from *SAR 1,000* and receive your share of rental returns.

✅ Officially documented ownership
✅ Quarterly rental returns
✅ Full transparency""",

    'q2': """*2. Are the properties real?*

Yes, we have *3 commercial and residential properties worth SAR 9M* in Riyadh, all pre-leased through Ejar government platform.

🏢 The company will acquire them and transfer ownership to investors via fractional ownership *after obtaining the official license from REGA*.""",

    'q3': """*3. What is the annual return?*

📈 Range: *6.71% to 10.16%*
📊 Average: *8.44% annually*

Note: All rates shown are *gross returns* before management fees.

🔄 Returns distributed *quarterly* to investor account.""",

    'q4': """*4. Is the company licensed?*

The company holds:
📄 *FAL Brokerage License:* 1200027650
📄 *Property Management License:* 2200003901
📄 *Ejar membership, Chamber of Commerce, and Maroof certificate*

⚠️ *Regulatory status:* We are an applicant in REGA's regulatory sandbox program. *We have NOT yet been granted a license to operate fractional real estate activities.*

📌 Actual operations (share sales, fund collection, ownership transfers, distributions) will only commence after the official license is issued.""",

    'q5': """*5. How to contact us?*

📧 *Official Email:* info@juzabilmia.com
🤖 *Telegram:* @JuzBilmia2026_bot
🌐 *Website:* juzabilmia.com

⏰ Bot available 24/7
🕒 Office: Sun-Thu, 9 AM - 6 PM""",

    'q6': """*6. What are the management fees?*

💼 *Management Fee:* 5% of annual rental
🔧 *Maintenance Fund:* 5% of total rental

━━━━━━━━━━━━━━━

📊 *Total deductions: 10% of rental*
(5% management + 5% maintenance)

Note: These are separate — maintenance fund covers property costs, not part of management fees.""",

    'q7': """*7. How can I sell my share?*

⏳ After *1 year* of ownership, you can request to sell.

💰 *Exit commission:* 1% of transaction value
📅 *Transfer period:* Within 14 business days

✅ Clear and transparent exit mechanism""",

    'q8': """*8. Is the displayed return net or gross?*

Displayed return is *gross*.

📊 *Net Return* = Gross return minus:
- Management fees (5%)
- Maintenance fund (5%)
= 10% deduction from rental

━━━━━━━━━━━━━━━

📌 *Example:*
10.16% gross ≈ *9.14% net*

🔄 Distributed *quarterly* to investor account.""",

    'q9': """*9. What is the minimum investment?*

💰 *Minimum: SAR 1,000*
(Single unit price)

✅ Buy any number of units per your budget
✅ Suitable for a wide range of investors""",

    'q10': """*10. What about tax on returns?*

The company is *officially registered for VAT* with ZATCA.

🧾 *VAT Number:* 314770310200003
📅 *Effective:* 01/06/2026

📊 15% VAT applies *only to management fees* per Article (36) of the VAT Implementing Regulations. The base share value (SAR 1,000) is exempt as an investment transaction.

📧 Details: *info@juzabilmia.com*""",

    'q11': """*11. Who covers maintenance costs?*

🛡️ Maintenance costs are *fully covered* by the maintenance fund

📊 *5%* deducted automatically from collected rent

✅ *Investor is NOT charged any additional amounts*""",

    'q12': """*12. Is payment secure?*

Yes, we use *Moyasar Financial Gateway*:

🏛️ Licensed by *SAMA (Central Bank)*
🛡️ *PCI-DSS* compliant

🔐 *Security:*
- SSL/TLS encryption for all transactions
- No card data storage (CVV/number/expiry)

💳 *Payment methods:*
✅ Mada | Visa | Mastercard | Apple Pay"""
}

# ========== الرسالة الافتراضية ==========
DEFAULT_AR = """💬 *حالياً ليس لدي معلومة مؤكدة عن هذا الاستفسار*

يشرفنا خدمتك والرد على سؤالك مباشرة عبر:

📧 *البريد الرسمي:*
info@juzabilmia.com

🌐 *الموقع:*
juzabilmia.com

أو يمكنك تصفح القائمة بالأسفل للمزيد من المعلومات 👇"""

DEFAULT_EN = """💬 *I don't have confirmed information about this yet*

We'd be honored to serve you and reply directly via:

📧 *Official Email:*
info@juzabilmia.com

🌐 *Website:*
juzabilmia.com

Or you can browse the menu below for more information 👇"""

# ========== إرسال الرسائل ==========
def send(chat_id, text, reply_markup=None):
    import json
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    requests.post(f"{API}/sendMessage", json=data)

def edit(chat_id, msg_id, text, reply_markup=None):
    import json
    data = {
        'chat_id': chat_id,
        'message_id': msg_id,
        'text': text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    requests.post(f"{API}/editMessageText", json=data)

def answer_cb(cb_id):
    requests.post(f"{API}/answerCallbackQuery", json={'callback_query_id': cb_id})

# ========== معالجة الرسائل النصية ==========
def smart_reply(text, lang):
    t = text.lower().strip()
    
    keywords_ar = {
        'platform_correction': ['منصة', 'منصه', 'هل انتم منصة', 'هل أنتم منصة', 'موقع منصة'],
        'about': ['عن الشركة', 'من انتم', 'من أنتم', 'تعريف', 'الشركة', 'مقر الشركة', 'مقركم', 'تأسست', 'تاسست', 'وين مقركم'],
        'how': ['كيف تعمل', 'الخطوات', 'كيف اشترك', 'كيف أبدأ', 'كيف ابدا', 'الاشتراك'],
        'portfolio': ['عقارات', 'محفظة', 'العقارات', 'المحفظة'],
        'calc': ['حاسبة', 'احسب', 'كم سأربح', 'كم العائد', 'حساب'],
        'features': ['ميزات', 'مميزات', 'لماذا'],
        'sharia': ['شرعي', 'شريعة', 'حلال', 'فتوى'],
        'licenses': ['ترخيص', 'تراخيص', 'مرخص', 'سجل تجاري', 'فال'],
        'payment': ['دفع', 'مدى', 'فيزا', 'ميسر', 'ميسّر', 'بطاقة', 'آمن'],
        'app': ['تطبيق', 'جوال', 'تحميل'],
        'faq': ['اسئلة', 'أسئلة', 'سؤال', 'استفسار'],
        'q9': ['الحد الادنى', 'الحد الأدنى', 'اقل مبلغ', 'أقل مبلغ', 'كم اقل', 'كم أقل'],
        'q3': ['كم العائد', 'كم الربح', 'العائد السنوي', 'الفائدة'],
        'q5': ['تواصل', 'اتصال', 'رقم', 'ايميل', 'بريد', 'هاتف'],
        'q7': ['بيع', 'تخارج', 'سحب', 'انسحب', 'استرداد']
    }
    
    keywords_en = {
        'platform_correction': ['platform', 'are you a platform'],
        'about': ['about', 'who are you', 'company', 'headquarter', 'founded', 'established'],
        'how': ['how does', 'how it works', 'steps', 'how to start', 'how to subscribe'],
        'portfolio': ['properties', 'portfolio'],
        'calc': ['calculator', 'how much will i earn', 'returns'],
        'features': ['features', 'why', 'benefits'],
        'sharia': ['sharia', 'halal', 'islamic'],
        'licenses': ['license', 'licensed', 'registration'],
        'payment': ['payment', 'pay', 'card', 'visa', 'mada', 'secure'],
        'app': ['app', 'mobile', 'download', 'android', 'ios'],
        'faq': ['faq', 'questions'],
        'q9': ['minimum', 'least amount', 'min investment'],
        'q3': ['return', 'profit', 'roi', 'yield'],
        'q5': ['contact', 'phone', 'email'],
        'q7': ['sell', 'exit', 'withdraw']
    }
    
    kw = keywords_ar if lang == 'ar' else keywords_en
    
    for key, words in kw.items():
        for word in words:
            if word in t:
                return key
    
    greetings_ar = ['مرحب', 'هلا', 'السلام', 'اهلا', 'أهلا', 'هاي', 'صباح', 'مساء']
    greetings_en = ['hi', 'hello', 'hey', 'good morning', 'good evening']
    greetings = greetings_ar if lang == 'ar' else greetings_en
    
    for g in greetings:
        if g in t:
            return 'welcome'
    
    return None

# ========== Webhook ==========
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'callback_query' in data:
        cb = data['callback_query']
        chat_id = cb['message']['chat']['id']
        msg_id = cb['message']['message_id']
        action = cb['data']
        cb_id = cb['id']
        
        answer_cb(cb_id)
        
        if action == 'lang_en':
            user_lang[chat_id] = 'en'
            edit(chat_id, msg_id, TEXTS_EN['welcome'], main_menu(chat_id))
            return "OK"
        if action == 'lang_ar':
            user_lang[chat_id] = 'ar'
            edit(chat_id, msg_id, TEXTS_AR['welcome'], main_menu(chat_id))
            return "OK"
        
        lang = L(chat_id)
        TEXTS = TEXTS_AR if lang == 'ar' else TEXTS_EN
        FAQ = FAQ_AR if lang == 'ar' else FAQ_EN
        
        if action == 'menu':
            edit(chat_id, msg_id, TEXTS['welcome'], main_menu(chat_id))
        elif action == 'faq':
            edit(chat_id, msg_id, TEXTS['faq'], faq_menu(chat_id))
        elif action in TEXTS:
            edit(chat_id, msg_id, TEXTS[action], back_btn(chat_id))
        elif action in FAQ:
            back_to_faq = {'inline_keyboard': [
                [{'text': '🔙 الأسئلة الشائعة' if lang == 'ar' else '🔙 FAQ', 'callback_data': 'faq'}],
                [{'text': '🏠 القائمة الرئيسية' if lang == 'ar' else '🏠 Main Menu', 'callback_data': 'menu'}]
            ]}
            edit(chat_id, msg_id, FAQ[action], back_to_faq)
        
        return "OK"
    
    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        lang = L(chat_id)
        
        if text in ['/start', '/menu']:
            TEXTS = TEXTS_AR if lang == 'ar' else TEXTS_EN
            send(chat_id, TEXTS['welcome'], main_menu(chat_id))
            return "OK"
        
        action = smart_reply(text, lang)
        TEXTS = TEXTS_AR if lang == 'ar' else TEXTS_EN
        FAQ = FAQ_AR if lang == 'ar' else FAQ_EN
        
        # دائماً نرد - حتى لو ما لقينا كلمة مفتاحية
        if action == 'welcome':
            send(chat_id, TEXTS['welcome'], main_menu(chat_id))
        elif action == 'faq':
            send(chat_id, TEXTS['faq'], faq_menu(chat_id))
        elif action and action in TEXTS:
            send(chat_id, TEXTS[action], back_btn(chat_id))
        elif action and action in FAQ:
            send(chat_id, FAQ[action], back_btn(chat_id))
        else:
            # رد افتراضي على أي سؤال غير معروف
            msg = DEFAULT_AR if lang == 'ar' else DEFAULT_EN
            send(chat_id, msg, main_menu(chat_id))
    
    return "OK"

@app.route('/')
def home():
    return "🤖 Juz Bilmia Bot v2.3 - Active!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
