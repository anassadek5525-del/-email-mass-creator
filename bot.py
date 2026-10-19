import os
import threading
import time
from supabase import create_client, Client

# قراءة المتغيرات السحابية من بيئة Railway
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# التحقق من وجود المتغيرات لمنع خطأ Invalid URL
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ خطأ: متغيرات Supabase غير موجودة أو غير مسجلة في البيئة السحابية!")

# إنشاء الاتصال بقاعدة البيانات
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("🚀 تم الاتصال بنجاح بقاعدة بيانات Supabase وبدء التشغيل!")

def worker_task(thread_id):
    """دالة لإنشاء الحسابات بالتوازي عبر الـ Threads"""
    print(f"🔥 Thread {thread_id} بدأ العمل...")
    # هنا يتم وضع منطق إنشاء الحسابات وإدخالها في Supabase
    while True:
        try:
            # مثال على عملية وهمية لإنشاء حساب وتخزينه
            time.sleep(2)
        except Exception as e:
            print(f"❌ خطأ في Thread {thread_id}: {e}")

if __name__ == "__main__":
    # تشغيل 50 Thread بالتوازي كما طلبت
    threads_count = 50
    print(f"⚡ جاري إطلاق {threads_count} خيط (Threads) للعمل في الخلفية...")
    
    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=worker_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
