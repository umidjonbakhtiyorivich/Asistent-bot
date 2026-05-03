#!/usr/bin/env python3
"""
SHAXSIY ASISTENT BOT
Umidjon aka uchun - Canary Group
"""

import logging
import sqlite3
import json
from datetime import datetime, timedelta
from threading import Thread
import time
import pytz

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# 🔑 BOT TOKEN
# ============================================
TELEGRAM_BOT_TOKEN = "8657222936:AAEMp7xZMumEMDpV9TRaLiptbGa4Dm1u9NM"

# Tashkent vaqti
TIMEZONE = pytz.timezone('Asia/Tashkent')


# ============================================
# 💾 DATABASE
# ============================================
class Database:
    def __init__(self, db_file="assistant.db"):
        self.db_file = db_file
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        """Database yaratish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tasks jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Reminders jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                remind_time TIMESTAMP NOT NULL,
                sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Notes jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized")
    
    # ==================== TASKS ====================
    
    def add_task(self, user_id, text):
        """Yangi vazifa qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, text) VALUES (?, ?)",
            (user_id, text)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id
    
    def get_tasks(self, user_id, completed=None):
        """Vazifalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if completed is None:
            cursor.execute(
                "SELECT id, text, completed, created_at FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
        else:
            cursor.execute(
                "SELECT id, text, completed, created_at FROM tasks WHERE user_id = ? AND completed = ? ORDER BY created_at DESC",
                (user_id, completed)
            )
        
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    
    def complete_task(self, user_id, task_id):
        """Vazifani bajarilgan deb belgilash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        rows = cursor.rowcount
        conn.commit()
        conn.close()
        return rows > 0
    
    def delete_task(self, user_id, task_id):
        """Vazifani o'chirish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        rows = cursor.rowcount
        conn.commit()
        conn.close()
        return rows > 0
    
    # ==================== REMINDERS ====================
    
    def add_reminder(self, user_id, text, remind_time):
        """Eslatma qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (user_id, text, remind_time) VALUES (?, ?, ?)",
            (user_id, text, remind_time.strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        reminder_id = cursor.lastrowid
        conn.close()
        return reminder_id
    
    def get_reminders(self, user_id, pending_only=True):
        """Eslatmalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if pending_only:
            cursor.execute(
                "SELECT id, text, remind_time, sent FROM reminders WHERE user_id = ? AND sent = 0 ORDER BY remind_time",
                (user_id,)
            )
        else:
            cursor.execute(
                "SELECT id, text, remind_time, sent FROM reminders WHERE user_id = ? ORDER BY remind_time DESC",
                (user_id,)
            )
        
        reminders = cursor.fetchall()
        conn.close()
        return reminders
    
    def get_due_reminders(self):
        """Vaqti kelgan eslatmalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(
            "SELECT id, user_id, text FROM reminders WHERE sent = 0 AND remind_time <= ?",
            (now,)
        )
        
        reminders = cursor.fetchall()
        conn.close()
        return reminders
    
    def mark_reminder_sent(self, reminder_id):
        """Eslatmani yuborilgan deb belgilash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reminders SET sent = 1 WHERE id = ?",
            (reminder_id,)
        )
        conn.commit()
        conn.close()
    
    def delete_reminder(self, user_id, reminder_id):
        """Eslatmani o'chirish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reminders WHERE id = ? AND user_id = ?",
            (reminder_id, user_id)
        )
        rows = cursor.rowcount
        conn.commit()
        conn.close()
        return rows > 0
    
    # ==================== NOTES ====================
    
    def add_note(self, user_id, text):
        """Not qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (user_id, text) VALUES (?, ?)",
            (user_id, text)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return note_id
    
    def get_notes(self, user_id):
        """Notlarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        notes = cursor.fetchall()
        conn.close()
        return notes
    
    def delete_note(self, user_id, note_id):
        """Notni o'chirish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?",
            (note_id, user_id)
        )
        rows = cursor.rowcount
        conn.commit()
        conn.close()
        return rows > 0
    
    # ==================== STATS ====================
    
    def get_stats(self, user_id):
        """Statistika"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Jami vazifalar
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,))
        total_tasks = cursor.fetchone()[0]
        
        # Bajarilgan vazifalar
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 1", (user_id,))
        completed_tasks = cursor.fetchone()[0]
        
        # Aktiv vazifalar
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = 0", (user_id,))
        active_tasks = cursor.fetchone()[0]
        
        # Eslatmalar
        cursor.execute("SELECT COUNT(*) FROM reminders WHERE user_id = ? AND sent = 0", (user_id,))
        pending_reminders = cursor.fetchone()[0]
        
        # Notlar
        cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
        total_notes = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'active_tasks': active_tasks,
            'pending_reminders': pending_reminders,
            'total_notes': total_notes
        }


# ============================================
# 📱 BOT LOGIC
# ============================================
db = Database()


def get_welcome_message(first_name):
    """Salom xabari"""
    return f"""
🤖 Assalomu alaykum, {first_name}!

Shaxsiy Asistent Bot ishga tushdi!

📋 FUNKSIYALAR:

✅ **Vazifalar:**
/task - Yangi vazifa
/tasks - Barcha vazifalar
/done [ID] - Bajarildi
/delete_task [ID] - O'chirish

⏰ **Eslatmalar:**
/remind - Yangi eslatma
/reminders - Barcha eslatmalar
/cancel_reminder [ID] - Bekor qilish

📝 **Notlar:**
/note - Tezkor not
/notes - Barcha notlar
/delete_note [ID] - Notni o'chirish

📊 **Boshqa:**
/stats - Statistika
/help - Yordam

Tayyor! 💪
"""


def handle_message(message_text, user_id, first_name, send_message_func):
    """Xabarlarni qayta ishlash"""
    
    # Buyruqlarni ajratish
    parts = message_text.strip().split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    # ==================== START ====================
    if command == '/start':
        return get_welcome_message(first_name)
    
    # ==================== HELP ====================
    elif command == '/help':
        return get_welcome_message(first_name)
    
    # ==================== TASKS ====================
    elif command == '/task':
        if not args:
            return "❌ Vazifa matnini yozing!\n\nMisol: /task Client bilan uchrashish"
        
        task_id = db.add_task(user_id, args)
        return f"✅ Vazifa qo'shildi! (ID: {task_id})\n\n📝 {args}"
    
    elif command == '/tasks':
        tasks = db.get_tasks(user_id, completed=0)
        
        if not tasks:
            return "📋 Hozircha vazifalar yo'q!\n\n/task buyrug'i bilan yangi vazifa qo'shing."
        
        response = "📋 **VAZIFALAR:**\n\n"
        for task in tasks:
            task_id, text, completed, created_at = task
            status = "✅" if completed else "⬜"
            response += f"{status} ID {task_id}: {text}\n"
        
        response += "\n💡 /done [ID] - Bajarildi\n💡 /delete_task [ID] - O'chirish"
        return response
    
    elif command == '/done':
        if not args.isdigit():
            return "❌ Vazifa ID sini yozing!\n\nMisol: /done 1"
        
        task_id = int(args)
        success = db.complete_task(user_id, task_id)
        
        if success:
            return f"✅ Vazifa #{task_id} bajarildi!"
        else:
            return f"❌ Vazifa #{task_id} topilmadi!"
    
    elif command == '/delete_task':
        if not args.isdigit():
            return "❌ Vazifa ID sini yozing!\n\nMisol: /delete_task 1"
        
        task_id = int(args)
        success = db.delete_task(user_id, task_id)
        
        if success:
            return f"🗑 Vazifa #{task_id} o'chirildi!"
        else:
            return f"❌ Vazifa #{task_id} topilmadi!"
    
    # ==================== REMINDERS ====================
    elif command == '/remind':
        if not args:
            return """
⏰ **ESLATMA QO'SHISH:**

/remind 18:00 Client bilan uchrashish
/remind 14:30 Reportni tayyorlash

Faqat vaqt va matnni yozing!
"""
        
        # Vaqt va matnni ajratish
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "❌ Noto'g'ri format!\n\nMisol: /remind 18:00 Client bilan uchrashish"
        
        time_str, text = parts
        
        try:
            # Vaqtni parse qilish
            hour, minute = map(int, time_str.split(':'))
            
            # Bugungi sana bilan birlashtirish
            now = datetime.now(TIMEZONE)
            remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Agar vaqt o'tib ketgan bo'lsa, ertaga qo'yamiz
            if remind_time <= now:
                remind_time += timedelta(days=1)
            
            reminder_id = db.add_reminder(user_id, text, remind_time)
            
            return f"⏰ Eslatma qo'shildi! (ID: {reminder_id})\n\n🕐 {time_str}\n📌 {text}"
        
        except Exception as e:
            return f"❌ Xato! Vaqtni to'g'ri yozing.\n\nMisol: /remind 18:00 Matn"
    
    elif command == '/reminders':
        reminders = db.get_reminders(user_id, pending_only=True)
        
        if not reminders:
            return "⏰ Hozircha eslatmalar yo'q!\n\n/remind buyrug'i bilan qo'shing."
        
        response = "⏰ **ESLATMALAR:**\n\n"
        for reminder in reminders:
            reminder_id, text, remind_time, sent = reminder
            response += f"🔔 ID {reminder_id}: {remind_time}\n📌 {text}\n\n"
        
        response += "💡 /cancel_reminder [ID] - Bekor qilish"
        return response
    
    elif command == '/cancel_reminder':
        if not args.isdigit():
            return "❌ Eslatma ID sini yozing!\n\nMisol: /cancel_reminder 1"
        
        reminder_id = int(args)
        success = db.delete_reminder(user_id, reminder_id)
        
        if success:
            return f"🗑 Eslatma #{reminder_id} bekor qilindi!"
        else:
            return f"❌ Eslatma #{reminder_id} topilmadi!"
    
    # ==================== NOTES ====================
    elif command == '/note':
        if not args:
            return "❌ Not matnini yozing!\n\nMisol: /note Bu muhim ma'lumot!"
        
        note_id = db.add_note(user_id, args)
        return f"📝 Not saqlandi! (ID: {note_id})\n\n{args}"
    
    elif command == '/notes':
        notes = db.get_notes(user_id)
        
        if not notes:
            return "📝 Hozircha notlar yo'q!\n\n/note buyrug'i bilan qo'shing."
        
        response = "📝 **NOTLAR:**\n\n"
        for note in notes:
            note_id, text, created_at = note
            response += f"📌 ID {note_id}: {text}\n"
        
        response += "\n💡 /delete_note [ID] - Notni o'chirish"
        return response
    
    elif command == '/delete_note':
        if not args.isdigit():
            return "❌ Not ID sini yozing!\n\nMisol: /delete_note 1"
        
        note_id = int(args)
        success = db.delete_note(user_id, note_id)
        
        if success:
            return f"🗑 Not #{note_id} o'chirildi!"
        else:
            return f"❌ Not #{note_id} topilmadi!"
    
    # ==================== STATS ====================
    elif command == '/stats':
        stats = db.get_stats(user_id)
        
        return f"""
📊 **STATISTIKA:**

✅ Vazifalar:
   • Jami: {stats['total_tasks']}
   • Bajarilgan: {stats['completed_tasks']}
   • Aktiv: {stats['active_tasks']}

⏰ Eslatmalar: {stats['pending_reminders']}

📝 Notlar: {stats['total_notes']}

💪 Ajoyib!
"""
    
    else:
        return "❓ Buyruqni tushunmadim. /help ni bosing."


# ============================================
# ⏰ REMINDER CHECKER
# ============================================
def check_reminders(send_message_func):
    """Eslatmalarni tekshirish va yuborish"""
    while True:
        try:
            # Vaqti kelgan eslatmalarni topish
            reminders = db.get_due_reminders()
            
            for reminder in reminders:
                reminder_id, user_id, text = reminder
                
                # Eslatmani yuborish
                message = f"⏰ **ESLATMA!**\n\n📌 {text}"
                send_message_func(user_id, message)
                
                # Yuborilgan deb belgilash
                db.mark_reminder_sent(reminder_id)
                
                logger.info(f"Sent reminder {reminder_id} to user {user_id}")
            
            # 30 soniya kutish
            time.sleep(30)
        
        except Exception as e:
            logger.error(f"Reminder checker error: {e}")
            time.sleep(60)


# ============================================
# 🚀 MAIN BOT
# ============================================
def main():
    """Botni ishga tushirish"""
    import requests
    
    # Token tekshirish
    if TELEGRAM_BOT_TOKEN == "SIZNING_TOKENINGIZNI_BU_YERGA_QOYING":
        print("❌ XATO: Token sozlanmagan!")
        return
    
    BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    
    def send_message(chat_id, text):
        """Xabar yuborish"""
        try:
            requests.post(
                f"{BASE_URL}/sendMessage",
                json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
            )
        except Exception as e:
            logger.error(f"Send message error: {e}")
    
    # Reminder checker ni alohida thread da ishga tushirish
    reminder_thread = Thread(target=check_reminders, args=(send_message,), daemon=True)
    reminder_thread.start()
    
    logger.info("✅ Shaxsiy Asistent Bot ishga tushdi!")
    logger.info("⏰ Reminder checker ishga tushdi!")
    
    offset = 0
    
    while True:
        try:
            # Yangi xabarlarni olish
            response = requests.get(
                f"{BASE_URL}/getUpdates",
                params={'offset': offset, 'timeout': 30}
            )
            
            if response.status_code == 200:
                updates = response.json().get('result', [])
                
                for update in updates:
                    offset = update['update_id'] + 1
                    
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        user_id = message['from']['id']
                        first_name = message['from'].get('first_name', 'Foydalanuvchi')
                        text = message.get('text', '')
                        
                        # Javob tayyorlash
                        reply = handle_message(text, user_id, first_name, send_message)
                        
                        # Javob yuborish
                        send_message(chat_id, reply)
                        
                        logger.info(f"Handled: {text} from {user_id}")
            
            time.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Bot to'xtatildi")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
