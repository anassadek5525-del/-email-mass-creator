import threading
import time
import random
import string
from supabase import create_client, Client

SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpeGh4aXd5amtqYmd5b29pY3VvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MjM2Njc2OCwiZXhwIjoyMTA3OTQyNzY4fQ.bfF-A4KvUvewLn9HdZpbe3EwGHAxXxTQ6-h4zzKq6IY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("🚀 تم الاتصال بنجاح بقاعدة بيانات Supabase وبدء التشغيل المستقر!")

def generate_random_account():
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(8))
    email = f"{name}@gmail.com"
    password = ''.join(random.choice(letters + string.digits) for i in range(10))
    return {"email": email, "password": password}

def worker_task(thread_id):
    print(f"🔥 Thread {thread_id} بدأ العمل في وضع الدفعات المستقرة...")
    
    while True:
        try:
            # تجهيز دفعة من 10 حسابات لكل خيط في المرة الواحدة
            batch_data = [generate_random_account() for _ in range(10)]
            
            # إرسال الدفعة دفعة واحدة لتقليل الضغط على السيرفر
            supabase.table("accounts").insert(batch_data).execute()
            
            print(f"✅ [Thread {thread_id}] تم إضافة دفعة (10 حسابات) بنجاح")
            
            # استراحة قصيرة جداً لتجنب حظر الاتصالات
            time.sleep(0.5)
            
        except Exception as e:
            print(f"⚠️ تنبيه في Thread {thread_id}: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threads_count = 30  # تقليل عدد الخيوط قليلاً لضمان الاستقرار التام وعدم قطع الاتصال
    print(f"⚡ جاري إطلاق {threads_count} خيط للعمل باستقرار تام...")
    
    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=worker_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
