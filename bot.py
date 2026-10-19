import threading
import time
import random
import string
from supabase import create_client, Client

# بيانات الاتصال بقاعدة البيانات
SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpeGh4aXd5amtqYmd5b29pY3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MjM2Njc2OCwiZXhwIjoyMTA3OTQyNzY4fQ.bfF-A4KvUvewLn9HdZpbe3EwGHAxXxTQ6-h4zzKq6IY"

print(f"🔗 جاري الاتصال برابط Supabase: {SUPABASE_URL}")

# إنشاء الاتصال
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("🚀 تم الاتصال بنجاح بقاعدة بيانات Supabase وبدء التشغيل!")

def generate_random_account():
    """توليد إيميل وباسوورد عشوائي لعملية التسجيل"""
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(8))
    email = f"{name}@gmail.com"
    password = ''.join(random.choice(letters + string.digits) for i in range(10))
    return email, password

def worker_task(thread_id):
    """دالة الـ Thread لإنشاء الحسابات ورفعها مباشرة لـ Supabase"""
    print(f"🔥 Thread {thread_id} بدأ العمل وجاري إنشاء الحسابات...")
    
    while True:
        try:
            # 1. توليد بيانات الحساب الجديد
            email, password = generate_random_account()
            
            # 2. إرسال البيانات للجدول في Supabase
            response = supabase.table("accounts").insert({
                "email": email,
                "password": password
            }).execute()
            
            print(f"✅ [Thread {thread_id}] تم إضافة الحساب بنجاح: {email}")
            
            # فاصل بسيط بين كل عملية إدخال عشان السيرفر ما يحصلش عليه ضغط مفاجئ
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ خطأ في Thread {thread_id}: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threads_count = 50
    print(f"⚡ جاري إطلاق {threads_count} خيط (Threads) للبدء في حفظ الحسابات...")
    
    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=worker_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
