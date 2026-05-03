# 🤖 SHAXSIY ASISTENT BOT

Professional shaxsiy asistent - Canary Group uchun maxsus!

---

## ✨ FUNKSIYALAR:

### ✅ Vazifalar (To-Do List)
- `/task [matn]` - Yangi vazifa qo'shish
- `/tasks` - Barcha vazifalarni ko'rish
- `/done [ID]` - Vazifani bajarilgan deb belgilash
- `/delete_task [ID]` - Vazifani o'chirish

**Misol:**
```
/task Client bilan uchrashish
/tasks
/done 1
/delete_task 2
```

---

### ⏰ Eslatmalar (Reminders)
- `/remind [vaqt] [matn]` - Yangi eslatma
- `/reminders` - Barcha eslatmalar
- `/cancel_reminder [ID]` - Eslatmani bekor qilish

**Misol:**
```
/remind 18:00 Client bilan uchrashish
/remind 14:30 Reportni tayyorlash
/reminders
/cancel_reminder 1
```

**Qanday ishlaydi:**
- Siz `/remind 18:00 Text` yuborsangiz
- Bot 18:00 da sizga avtomatik eslatma yuboradi!
- 24/7 ishlab turadi - hech qachon unutmaysiz!

---

### 📝 Notlar (Quick Notes)
- `/note [matn]` - Tezkor not saqlash
- `/notes` - Barcha notlar
- `/delete_note [ID]` - Notni o'chirish

**Misol:**
```
/note Bu muhim ma'lumot!
/note Client telefon: +998901234567
/notes
/delete_note 1
```

---

### 📊 Statistika
- `/stats` - Umumiy statistika

---

## 🚀 O'RNATISH:

### 1️⃣ BotFather da yangi bot yarating

Telegram da `@BotFather` ga o'ting:
```
/newbot
Bot nomi: Shaxsiy Asistent
Username: my_assistant_bot
```

Tokenni copy qiling!

---

### 2️⃣ Kodga tokenni qo'ying

`assistant_bot.py` faylini oching:

```python
TELEGRAM_BOT_TOKEN = "SIZNING_TOKENINGIZ"
```

---

### 3️⃣ O'rnatish

**Lokal (kompyuteringizda):**
```bash
pip install -r assistant_requirements.txt
python assistant_bot.py
```

**Render.com (24/7 ishlash):**
1. GitHub repository yarating
2. Bu fayllarni yuklang
3. Render.com da deploy qiling
4. Environment variable: `TELEGRAM_BOT_TOKEN`

---

## 💾 DATABASE:

Bot **SQLite** database ishlatadi.

**Avtomatik yaratiladi:**
- `assistant.db` fayli
- 3 ta jadval: tasks, reminders, notes

**Barcha ma'lumotlar saqlanadi!**

---

## ⏰ REMINDER SYSTEM:

Bot alohida **thread** da har 30 soniyada eslatmalarni tekshiradi.

Vaqti kelgan eslatma **avtomatik yuboriladi!**

---

## 📱 ISHLATISH:

### Vazifalar:
```
/task Klient bilan zoom meeting
/task Instagram post tayyorlash
/task Reportni yuborish
/tasks
```

**Natija:**
```
📋 VAZIFALAR:

⬜ ID 1: Klient bilan zoom meeting
⬜ ID 2: Instagram post tayyorlash
⬜ ID 3: Reportni yuborish

💡 /done [ID] - Bajarildi
💡 /delete_task [ID] - O'chirish
```

### Bajarildi:
```
/done 1
```

**Natija:**
```
✅ Vazifa #1 bajarildi!
```

---

### Eslatmalar:
```
/remind 18:00 Zoom meeting
/remind 14:30 Lunch break
/reminders
```

**18:00 da bot yuboradi:**
```
⏰ ESLATMA!

📌 Zoom meeting
```

---

### Notlar:
```
/note Client telefon: +998901234567
/note API key: abc123xyz
/notes
```

---

### Statistika:
```
/stats
```

**Natija:**
```
📊 STATISTIKA:

✅ Vazifalar:
   • Jami: 10
   • Bajarilgan: 7
   • Aktiv: 3

⏰ Eslatmalar: 2

📝 Notlar: 5

💪 Ajoyib!
```

---

## 🎯 KEYINGI BOSQICHLAR:

### BOSQICH 2 (Kelgusi hafta):
- ✅ Inline tugmalar
- ✅ Client management
- ✅ Lead tracking
- ✅ Kunlik/haftalik reportlar

### BOSQICH 3:
- ✅ ChatGPT integration
- ✅ DALL-E rasm yaratish
- ✅ Ovozli xabarlar
- ✅ Calendar integration

---

## 💡 TIPS:

1. **Vazifalarni muntazam tekshiring:** `/tasks`
2. **Eslatmalardan foydalaning:** Muhim uchrashuvlar uchun
3. **Notlarga muhim ma'lumot saqlang:** Parollar, telefonlar
4. **Statistikani kuzating:** `/stats` - progress ko'ring!

---

## 🐛 TROUBLESHOOTING:

**Bot javob bermasa:**
1. Tokenni tekshiring
2. Bot ishlab turibdimi? (`python assistant_bot.py`)
3. Render.com da logs ni ko'ring

**Eslatma kelmasa:**
1. Vaqtni to'g'ri yozganingizni tekshiring (HH:MM)
2. Bot 24/7 ishlab turishi kerak

---

## 📞 SUPPORT:

Savol yoki muammo bo'lsa - Claude (Jarvis) ga murojaat qiling! 💪

---

**Made with ❤️ for Canary Group**

