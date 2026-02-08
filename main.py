import requests
import random
import re

# --- لیست آی‌پی‌های تمیز و دامنه‌های فرانچایز (مخصوص ایرانسل و همراه اول) ---
# این‌ها تست شده هستند
CLEAN_IPS = [
    "www.visa.com", 
    "www.udemy.com", 
    "discord.com", 
    "cdn.discordapp.com",
    "104.16.200.200", 
    "162.159.135.42",
    "198.41.200.200",
    "172.64.152.14"
]

# --- منابع کانفیگ (بهترین‌های گیت‌هاب) ---
SOURCES = [
    # ریلیتی (بهترین سرعت - بدون نیاز به تغییر)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    # وی‌لس (نیاز به تزریق آی‌پی)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    # میکس (کمکی)
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_data(url):
    try:
        resp = requests.get(url, timeout=10)
        return resp.text if resp.status_code == 200 else ""
    except:
        return ""

def main():
    print("🚀 Starting Sniper Mode...")
    
    final_configs = []
    
    for url in SOURCES:
        data = get_data(url)
        lines = data.splitlines()
        
        for line in lines:
            line = line.strip()
            if len(line) < 10: continue

            # --- استراتژی 1: Reality (طلا) ---
            # اگر ریلیتی است، دست نزن و مستقیم اضافه کن
            if "reality" in line or "pbk=" in line:
                if "#" not in line: line += "#💎_Reality"
                final_configs.append(line)
                continue

            # --- استراتژی 2: VLESS (نقره) ---
            # اگر VLESS معمولی است، آی‌پی تمیز تزریق کن
            if line.startswith("vless://") and "type=ws" in line:
                try:
                    # انتخاب آی‌پی تمیز
                    clean_ip = random.choice(CLEAN_IPS)
                    
                    # پارس کردن لینک با Regex دقیق
                    # هدف: پیدا کردن آدرس فعلی و جایگزینی آن
                    # ساختار: vless://UUID@ADDRESS:PORT?PARAMS
                    match = re.search(r'vless://(?P<uuid>.*?)@(?P<addr>.*?):(?P<port>.*?)\?(?P<params>.*)', line)
                    
                    if match:
                        uuid = match.group("uuid")
                        old_addr = match.group("addr")
                        port = match.group("port")
                        params = match.group("params")
                        
                        # نام گذاری
                        name = line.split("#")[1] if "#" in line else "MCI_Turbo"

                        # اگر SNI یا Host در پارامترها نبود، آدرس قبلی را SNI کن
                        if "sni=" not in params: params += f"&sni={old_addr}"
                        if "host=" not in params: params += f"&host={old_addr}"
                        
                        # ساخت لینک جدید با آی‌پی تمیز
                        new_link = f"vless://{uuid}@{clean_ip}:{port}?{params}#{name}"
                        final_configs.append(new_link)
                except:
                    continue

    # اگر لیست خالی شد (محض احتیاط)
    if not final_configs:
        final_configs.append("vless://uuid@127.0.0.1:443?encryption=none&security=tls&type=ws&sni=google.com#ERROR")

    # مخلوط کردن
    random.shuffle(final_configs)
    
    # ذخیره 100 تای برتر
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs[:100]))
        
    print("✅ Done.")

if __name__ == "__main__":
    main()
