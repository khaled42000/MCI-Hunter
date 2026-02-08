import requests
import random
import re
import base64

# --- منابع (آپدیت شده و تضمینی) ---
CLEAN_IP_SOURCES = [
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_mci",
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_irancell",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt" # منبع کمکی
]

CONFIG_SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Iranian-V2Ray/configs/main/v2ray"
]

def get_content(url):
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"! Error fetching {url}: {e}")
    return ""

def get_clean_ips():
    print("--- Searching for Clean IPs ---")
    ips = []
    for source in CLEAN_IP_SOURCES:
        text = get_content(source)
        # الگوی دقیق برای پیدا کردن IP (عدد.عدد.عدد.عدد)
        found = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
        ips.extend(found)
        print(f"  + Found {len(found)} IPs from {source}")
    
    unique_ips = list(set(ips))
    # حذف آی‌پی‌های لوکال و نامعتبر
    clean = [ip for ip in unique_ips if not ip.startswith('127.') and not ip.startswith('0.')]
    print(f"Total Unique Clean IPs: {len(clean)}")
    return clean

def get_configs():
    print("--- Collecting Configs ---")
    configs = []
    for source in CONFIG_SOURCES:
        text = get_content(source)
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            # فیلتر کردن کانفیگ‌های معتبر
            if line.startswith("vless://") or line.startswith("vmess://") or line.startswith("trojan://"):
                 configs.append(line)
        print(f"  + Collected configs from {source}")
    
    # حذف تکراری‌ها
    unique_configs = list(set(configs))
    print(f"Total Raw Configs: {len(unique_configs)}")
    return unique_configs

def main():
    clean_ips = get_clean_ips()
    raw_configs = get_configs()

    # اگر آی‌پی پیدا نشد، از چند آی‌پی معروف کلودفلر استفاده کن
    if not clean_ips:
        print("! Warning: No clean IPs found. Using defaults.")
        clean_ips = ['104.16.200.200', '162.159.135.42', '198.41.200.200']

    final_configs = []
    
    print("--- Injecting IPs ---")
    for conf in raw_configs:
        # ما فقط روی VLESS و Reality تمرکز می‌کنیم چون برای تزریق راحت‌ترند
        if "vless://" in conf:
            try:
                # استخراج اطلاعات لینک با Regex (روش مطمئن‌تر)
                # vless://UUID@HOST:PORT?PARAMS#NAME
                match = re.search(r'vless://([^@]+)@([^:]+):(\d+)\?([^#]+)(?:#(.*))?', conf)
                
                if match:
                    uuid = match.group(1)
                    original_host = match.group(2)
                    port = match.group(3)
                    params = match.group(4)
                    name = match.group(5) if match.group(5) else "Config"

                    # انتخاب آی‌پی تمیز
                    random_ip = random.choice(clean_ips)
                    
                    # اطمینان از وجود SNI و HOST در پارامترها
                    new_params = params
                    if "sni=" not in new_params: new_params += f"&sni={original_host}"
                    if "host=" not in new_params: new_params += f"&host={original_host}"
                    
                    # ساخت لینک جدید
                    new_link = f"vless://{uuid}@{random_ip}:{port}?{new_params}#🚀_MCI_{name}"
                    final_configs.append(new_link)
                else:
                    # اگر نتوانستیم تزریق کنیم، خود کانفیگ اصلی را اضافه کن (به عنوان زاپاس)
                    final_configs.append(conf)
            except Exception as e:
                # در صورت هرگونه خطا، کانفیگ خام را نگه دار
                final_configs.append(conf)
        else:
            # کانفیگ‌های VMess و Trojan را بدون تغییر اضافه کن (چون تزریقشان سخت است)
            final_configs.append(conf)

    print(f"Final Processed Configs: {len(final_configs)}")

    # اگر لیست نهایی خالی بود (که محال است)، حداقل یک پیام خطا بنویس
    if not final_configs:
        final_configs = ["vless://uuid@127.0.0.1:443?encryption=none&security=tls&type=ws&host=example.com&sni=example.com#ERROR_NO_CONFIGS"]

    # مخلوط کردن لیست
    random.shuffle(final_configs)
    
    # محدود کردن به 150 تا (برای جلوگیری از هنگ کردن کلاینت)
    output_list = final_configs[:150]

    # ذخیره در فایل sub.txt
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_list))
    
    print(">>> SUCCESS: sub.txt generated!")

if __name__ == "__main__":
    main()
