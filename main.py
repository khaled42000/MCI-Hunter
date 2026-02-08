import requests
import random
import re
import os

# --- تنظیمات ---
# منابع آی‌پی تمیز
IP_SOURCES = [
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_mci",
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_irancell",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/donated"
]

# منابع کانفیگ
CONFIG_SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_content(url):
    try:
        # هدر مرورگر برای جلوگیری از مسدود شدن
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except:
        return ""
    return ""

def main():
    print("🚀 Starting Process...")

    # 1. جمع‌آوری آی‌پی‌های تمیز
    clean_ips = []
    for src in IP_SOURCES:
        text = get_content(src)
        found = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        clean_ips.extend(found)
    
    # حذف تکراری‌ها و آی‌پی‌های لوکال
    clean_ips = list(set([ip for ip in clean_ips if not ip.startswith("127.") and not ip.startswith("0.")]))
    
    if not clean_ips:
        # آی‌پی زاپاس (اگر هیچی پیدا نشد)
        clean_ips = ['104.16.200.200', '162.159.135.42']

    print(f"✅ Loaded {len(clean_ips)} Clean IPs")

    # 2. جمع‌آوری و پردازش کانفیگ‌ها
    final_configs = []
    
    for src in CONFIG_SOURCES:
        text = get_content(src)
        lines = text.splitlines()
        
        for line in lines:
            line = line.strip()
            if len(line) < 10: continue

            try:
                # --- استراتژی ریلیتی (دست نخورد) ---
                if "pbk=" in line or "fp=" in line and "type=grpc" in line:
                    final_configs.append(line)
                    continue

                # --- استراتژی تزریق (فقط VLESS + WS) ---
                if line.startswith("vless://") and "type=ws" in line:
                    # چک کردن اینکه لینک سالم است (حتما @ و : داشته باشد)
                    if "@" in line and ":" in line:
                        # انتخاب آی‌پی تمیز
                        ip = random.choice(clean_ips)
                        
                        # جایگزینی آی‌پی با Regex امن
                        # فقط آی‌پی بین @ و : را عوض می‌کند
                        line = re.sub(r'@(.*?):', f'@{ip}:', line, 1)
                        
                        # تغییر نام برای زیبایی
                        if "#" in line:
                            line = line.split("#")[0] + f"#🚀_MCI_TURBO_{random.randint(1,999)}"
                        else:
                            line += f"#🚀_MCI_TURBO_{random.randint(1,999)}"
                            
                        final_configs.append(line)
                    else:
                        # لینک خراب بود، ردش کن
                        continue
                
                # --- سایر پروتکل‌ها (Trojan/Shadowsocks) ---
                elif line.startswith("trojan://") or line.startswith("ss://"):
                    final_configs.append(line)

            except Exception:
                # اگر هر خطایی در پردازش این خط رخ داد، نادیده بگیر و برو بعدی
                # این باعث می‌شود برنامه هرگز کرش نکند
                continue

    # 3. ذخیره نهایی
    if not final_configs:
        # محض احتیاط اگر لیست خالی شد
        final_configs = ["vless://uuid@127.0.0.1:443?encryption=none&security=tls&type=ws&host=google.com&sni=google.com#BACKUP_CONFIG"]

    random.shuffle(final_configs)
    # نوشتن فایل
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs[:150]))

    print("🎉 Done! sub.txt updated.")

if __name__ == "__main__":
    main()
