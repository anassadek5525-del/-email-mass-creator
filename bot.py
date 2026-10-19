import threading
import time
from supabase import create_client, Client

# كتابة البيانات المباشرة والصحيحة لمنع أي خطأ في قراءة البيئة
SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "sb_secret_tJDsNRcd128YttRNWQvIXg_LFFuhm28"

print(f"🔗 جاري الاتصال برابط Supabase: {SUPABASE_URL}")

# إنشاء الاتصال بقاعدة البيانات
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("🚀 تم الاتصال بنجاح بقاعدة بيانات Supabase وبدء التشغيل!")

def worker_task(thread_id):
    """دالة لإنشاء الحسابات بالتوازي عبر الـ Threads"""
    print(f"🔥 Thread {thread_id} بدأ العمل...")
    while True:
        try:
            # هنا منطق العمل الخاص بإنشاء الحسابات
            time.sleep(2)
        except Exception as e:
            print(f"❌ خطأ في Thread {thread_id}: {e}")

if __name__ == "__main__":
    threads_count = 50
    print(f"⚡ جاري إطلاق {threads_count} خيط (Threads) للعمل في الخلفية...")
    
    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=worker_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
