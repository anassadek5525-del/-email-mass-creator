import concurrent.futures
import random
import string
import time
import os
from supabase import create_client, Client

# قراءة بيانات الاتصال بـ Supabase من متغيرات البيئة السحابية (أمان تام)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TOTAL_ACCOUNTS_TARGET = 200000
NUM_THREADS = 50
accounts_created = 0

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_single_account(thread_id):
    global accounts_created
    
    while True:
        if accounts_created >= TOTAL_ACCOUNTS_TARGET:
            return

        try:
            username = f"user_{generate_random_string(10)}"
            email = f"{username}@your-sending-domain.com"
            password = generate_random_string(12)
            
            # محاكاة وقت طلب التسجيل
            time.sleep(random.uniform(10, 15))

            data = {
                "email": email,
                "password": password,
                "smtp_host": "smtp.your-provider.com",
                "smtp_port": 587,
                "daily_sent_count": 0,
                "max_daily_limit": 5,
                "status": "active"
            }
            
            response = supabase.table("sender_accounts").insert(data).execute()
            
            if response.data:
                accounts_created += 1
                print(f"[Thread {thread_id}] 🟢 تم إنشاء الحساب: {email} | الإجمالي: {accounts_created}")

        except Exception as e:
            print(f"[Thread {thread_id}] ❌ خطأ: {str(e)}")
            time.sleep(5)

def start_mass_creation():
    print(f"🚀 بدء انطلاق {NUM_THREADS} سكربت سحابي لإنشاء 200,000 حساب...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(create_single_account, i+1) for i in range(NUM_THREADS)]
        concurrent.futures.wait(futures)
        
    print("🎉 تم الانتهاء من إنشاء الـ 200,000 حساب بالكامل!")

if __name__ == "__main__":
    start_mass_creation()