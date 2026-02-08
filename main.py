import requests
import random
import re
import base64

# --- تنظیمات فوق سری ---
# لیست آی‌پی‌های تمیز کلودفلر (تست شده برای ایرانسل و همراه اول - آپدیت 2026)
CLEAN_IPS = [
    "www.visa.com", "www.udemy.com", "discord.com", "cdn.discordapp.com",
    "104.16.200.200", "162.159.135.42", "198.41.200.200", "172.64.152.14"
]

# منابع طلایی (این‌ها خودشان فیلتر شده و تمیز هستند)
SOURCES = [
    # منبع 1: فقط ریلیتی‌های سالم (VLESS Reality)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    # منبع 2: فقط تروجان‌های سالم (Trojan)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/trojan",
    # منبع 3: کانفیگ‌های میکس و تست شده
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_content(url):
    try:
        # هدر واقعی مرورگر کروم برای جلوگیری از مسدود شدن توسط گیت‌هاب
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except:
        return ""
    return ""

def main():
    print("🚀 Starting Ultimate Harvester...")
    
    final_configs = []
    seen_configs = set() # برای حذف تکراری‌ها

    for url in SOURCES:
        content = get_content(url)
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if len(line) < 10 or line in seen_configs: continue
            
            # فیلتر: حذف کانفیگ‌های لوکال و بی‌کیفیت
            if "127.0.0.1" in line or "localhost" in line: continue

            # --- سناریوی 1: کانفیگ‌های Reality (طلا) ---
            # این‌ها را اصلاً نباید دست زد، چون به آی‌پی حساسند.
            if "reality" in line or "pbk=" in line or "fp=" in line:
                if "#" not in line: line += "#💎_Reality"
                seen_configs.add(line)
                final_configs.append(line)
                continue

            # --- سناریوی 2: کانفیگ‌های VLESS معمولی (نقره) ---
            # فقط به این‌ها آی‌پی تمیز تزریق می‌کنیم
            if line.startswith("vless://") and "type=ws" in line:
                try:
                    # انتخاب آی‌پی تمیز
                    clean_ip = random.choice(CLEAN_IPS)
                    
                    # Regex برای تعویض فقط بخش آدرس (بین @ و :)
                    # این روش امن‌ترین روش جایگزینی است
                    new_line = re.sub(r'@(.*?):', f'@{clean_ip}:', line, 1)
                    
                    # مطمئن می‌شویم که SNI سرجایش است
                    if "sni=" not in new_line:
                        # تلاش برای پیدا کردن آدرس قدیمی به عنوان SNI
                        old_addr_match = re.search(r'@(.*?):', line)
                        if old_addr_match:
                            old_addr = old_addr_match.group(1)
                            if "?" in new_line: new_line += f"&sni={old_addr}&host={old_addr}"
                            else: new_line += f"?sni={old_addr}&host={old_addr}"
                    
                    # اسم‌گذاری
                    new_line = new_line.split("#")[0] + f"#🚀_Turbo_MCI"
                    
                    seen_configs.add(new_line)
                    final_configs.append(new_line)
                except:
                    continue

            # --- سناریوی 3: تروجان (برنز) ---
            # تروجان‌ها را هم بدون تغییر اضافه می‌کنیم (چون تزریق اغلب خرابشان می‌کند)
            elif line.startswith("trojan://"):
                if "#" not in line: line += "#🛡️_Trojan"
                seen_configs.add(line)
                final_configs.append(line)

    # اگر لیست خالی بود (محض احتیاط برای جلوگیری از کرش)
    if not final_configs:
        final_configs.append("vless://uuid@104.16.200.200:443?type=ws&sni=google.com#BACKUP")

    # مخلوط کردن لیست
    random.shuffle(final_configs)
    
    # محدود کردن به 100 عدد (برای سبک شدن فایل)
    output_configs = final_configs[:100]

    # ذخیره در فایل متنی ساده
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_configs))
        
    # ذخیره در فایل Base64 (برای برخی کلاینت‌های خاص)
    with open("sub_b64.txt", "w", encoding="utf-8") as f:
        encoded = base64.b64encode("\n".join(output_configs).encode("utf-8")).decode("utf-8")
        f.write(encoded)

    print(f"✅ Successfully gathered {len(output_configs)} configs.")

if __name__ == "__main__":
    main()
