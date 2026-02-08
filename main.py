import requests
import random
import re
import os

def get_data(url):
    try:
        # هدر واقعی مرورگر برای جلوگیری از بلاک شدن
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")
    return ""

def main():
    print("🚀 Starting MCI Hunter...")
    
    # 1. پیدا کردن آی‌پی‌های تمیز
    clean_ips = []
    ip_sources = [
        "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_mci",
        "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_irancell"
    ]
    
    for src in ip_sources:
        text = get_data(src)
        # پیدا کردن الگوی آی‌پی
        found = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        clean_ips.extend(found)
    
    clean_ips = list(set(clean_ips))
    # حذف لوکال‌ها
    clean_ips = [ip for ip in clean_ips if not ip.startswith("127.") and not ip.startswith("0.")]
    
    if not clean_ips:
        print("⚠️ No clean IPs found! Using backup IPs.")
        clean_ips = ['104.16.200.200', '162.159.135.42'] # آی‌پی‌های زاپاس کلودفلر
    else:
        print(f"✅ Found {len(clean_ips)} clean IPs.")

    # 2. پیدا کردن کانفیگ‌ها
    raw_configs = []
    conf_sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
    ]

    for src in conf_sources:
        text = get_data(src)
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("vless://") or line.startswith("trojan://"):
                raw_configs.append(line)
    
    print(f"✅ Found {len(raw_configs)} raw configs.")

    # 3. تزریق و ساخت فایل نهایی
    final_list = []
    
    for conf in raw_configs:
        try:
            # اگر VLESS باشد تزریق می‌کنیم
            if "vless://" in conf:
                ip = random.choice(clean_ips)
                # جایگزینی ساده آی‌پی بین @ و :
                # Regex برای پیدا کردن قسمت آدرس
                conf = re.sub(r'@(.*?):', f'@{ip}:', conf, 1)
                
                if "#" not in conf: conf += "#MCI_Hunter"
                final_list.append(conf)
            else:
                final_list.append(conf)
        except:
            continue

    # اگر لیست خالی ماند (محض احتیاط)
    if not final_list:
        final_list = ["vless://uuid@104.16.200.200:443?encryption=none&security=tls&type=ws&host=dl.google.com&sni=dl.google.com#ERROR_BACKUP"]

    # ذخیره فایل
    random.shuffle(final_list)
    # نوشتن فایل
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list[:150]))
        
    print("🎉 sub.txt created successfully!")

if __name__ == "__main__":
    main()
