import threading
import time
import random
import string
from supabase import create_client, Client

# بيانات الاتصال بقاعدة البيانات
SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "sb_secret_tJDsNRcd128YttRNWQvIXg_LFFuhm28"

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
