import requests
import re
import random
import base64
import os

# --- منابع طلایی و تضمینی ---
SOURCES = [
    # منبع 1: ریلیتی‌های تست شده (بهترین سرعت در ایران)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    # منبع 2: کانفیگ‌های میکس (تروجان و وی‌لس)
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    # منبع 3: کانفیگ‌های مخصوص همراه اول و ایرانسل
    "https://raw.githubusercontent.com/Iranian-V2Ray/configs/main/v2ray"
]

# --- آی‌پی‌های تمیز کلودفلر (جهت تزریق به VLESS) ---
CLEAN_IPS = [
    "www.visa.com", "www.udemy.com", "discord.com", "cdn.discordapp.com",
    "104.16.200.200", "162.159.135.42", "198.41.200.200", "172.64.152.14"
]

def fetch_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except:
        return ""
    return ""

def main():
    print("🚀 Starting Master Harvester...")
    
    unique_configs = set()
    final_list = []

    for url in SOURCES:
        content = fetch_url(url)
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if len(line) < 10: continue
            if "vmess://" in line: continue # حذف VMess (چون معمولاً کند است)

            # --- استراتژی 1: Reality (دست نزن!) ---
            # این‌ها حساس هستند. اگر دست بزنیم قطع می‌شوند.
            if "reality" in line or "pbk=" in line:
                # فقط یک اسم زیبا بهش اضافه می‌کنیم
                if "#" in line:
                    parts = line.split("#")
                    line = parts[0] + f"#{parts[1]}_Reality"
                else:
                    line += "#💎_Reality"
                
                if line not in unique_configs:
                    unique_configs.add(line)
                    final_list.append(line)
                continue

            # --- استراتژی 2: VLESS معمولی (تزریق آی‌پی) ---
            if line.startswith("vless://") and "type=ws" in line:
                try:
                    # انتخاب آی‌پی تمیز
                    clean_ip = random.choice(CLEAN_IPS)
                    
                    # جایگزینی آی‌پی (فقط بخش بین @ و :)
                    # این Regex بسیار امن است و لینک را خراب نمی‌کند
                    new_line = re.sub(r'@(.*?):', f'@{clean_ip}:', line, 1)
                    
                    # مطمئن می‌شویم SNI دارد
                    if "sni=" not in new_line:
                        # پیدا کردن آدرس قدیمی برای استفاده به عنوان SNI
                        old_match = re.search(r'@(.*?):', line)
                        if old_match:
                            old_addr = old_match.group(1)
                            joiner = "&" if "?" in new_line else "?"
                            new_line += f"{joiner}sni={old_addr}&host={old_addr}"
                    
                    # تغییر نام
                    new_line = new_line.split("#")[0] + f"#🚀_Turbo_MCI"
                    
                    if new_line not in unique_configs:
                        unique_configs.add(new_line)
                        final_list.append(new_line)
                except:
                    continue

            # --- استراتژی 3: Trojan (دست نزن) ---
            elif line.startswith("trojan://"):
                if line not in unique_configs:
                    unique_configs.add(line)
                    final_list.append(line)

    # شافل کردن (بر زدن)
    random.shuffle(final_list)
    
    # انتخاب 100 تای برتر
    output = final_list[:100]
    
    # اگر لیست خالی بود (محال است، ولی برای اطمینان)
    if not output:
        output = ["vless://uuid@127.0.0.1:443?type=ws&sni=google.com#ERROR_NO_CONFIGS"]

    # ذخیره در فایل
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"✅ Success! Saved {len(output)} configs.")

if __name__ == "__main__":
    main()
