import requests
import random
import re
import base64

# --- تنظیمات ---
# پورت‌های مجاز کلودفلر (فقط این‌ها اجازه تزریق دارند)
CF_PORTS = ['443', '2053', '2083', '2087', '2096', '8443', '80', '8080', '8880', '2052', '2082', '2086', '2095']

# منابع آی‌پی تمیز (مخصوص ایران)
IP_SOURCES = [
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_mci",      # همراه اول
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_irancell", # ایرانسل
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/donated" # آی‌پی‌های اهدایی
]

# منابع کانفیگ
CONFIG_SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality", # ریلیتی (دست نخورد)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",   # مناسب تزریق
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_text(url):
    try:
        headers = {'User-Agent': 'v2rayNG'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.text
    except:
        pass
    return ""

def main():
    print("🚀 Starting Smart Hunter...")

    # 1. دریافت آی‌پی‌های تمیز
    clean_ips = []
    for src in IP_SOURCES:
        text = get_text(src)
        # یافتن آی‌پی‌ها
        found = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        clean_ips.extend(found)
    
    # حذف لوکال و تکراری
    clean_ips = list(set([ip for ip in clean_ips if not ip.startswith("127.")]))
    
    if not clean_ips:
        clean_ips = ['104.16.200.200', '162.159.135.42'] # آی‌پی زاپاس
    
    print(f"✅ Found {len(clean_ips)} Clean IPs")

    # 2. دریافت و پردازش کانفیگ‌ها
    final_configs = []
    
    for src in CONFIG_SOURCES:
        text = get_text(src)
        lines = text.splitlines()
        
        for line in lines:
            line = line.strip()
            
            # --- استراتژی 1: ریلیتی (Reality) ---
            # این‌ها را اصلاً دست نزن، چون خراب می‌شوند. مستقیم اضافه کن.
            if "pbk=" in line or "fp=" in line and "sni=" in line and "type=grpc" in line:
                if "#" not in line: line += "#💎_Reality_Original"
                final_configs.append(line)
                continue

            # --- استراتژی 2: تزریق هوشمند (Smart Injection) ---
            # فقط روی VLESS هایی که Websocket هستند و پورت استاندارد دارند اجرا شود
            if line.startswith("vless://") and "type=ws" in line:
                try:
                    # استخراج پورت
                    # vless://uuid@ip:PORT?params
                    part_address = line.split("@")[1]
                    port = part_address.split("?")[0].split(":")[1]
                    
                    # اگر پورت جزو پورت‌های کلودفلر بود، تزریق کن
                    if port in CF_PORTS:
                        ip = random.choice(clean_ips)
                        # Regex برای جایگزینی فقط بخش آی‌پی
                        # پیدا کردن چیزی بین @ و :
                        line = re.sub(r'@(.*?):', f'@{ip}:', line, 1)
                        
                        # مطمئن شویم SNI و HOST وجود دارد (برای جلوگیری از اختلال)
                        # استخراج هاست اصلی از کانفیگ
                        # معمولاً host=domain.com یا sni=domain.com است
                        # اگر نداشت، این کانفیگ به درد تزریق نمی‌خورد، ردش می‌کنیم
                        if "sni=" in line or "host=" in line:
                            # تغییر نام
                            line = line.split("#")[0] + f"#🚀_Turbo_{random.randint(100,999)}"
                            final_configs.append(line)
                    else:
                        # اگر پورتش استاندارد نبود، دست نزن و خود کانفیگ را بگذار
                        final_configs.append(line)
                except:
                    continue
            
            # --- استراتژی 3: سایر موارد (Trojan, VMess) ---
            # این‌ها را هم به عنوان زاپاس نگه دار (بدون تغییر)
            elif line.startswith("trojan://") or line.startswith("ss://"):
                final_configs.append(line)

    # شافل کردن برای تنوع
    random.shuffle(final_configs)
    
    # محدود کردن تعداد (100 تای اول)
    output = final_configs[:100]

    # ذخیره فایل
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"🎉 Success! Generated {len(output)} valid configs.")

if __name__ == "__main__":
    main()
