import requests
import random

# --- لیست آی‌پی‌های تمیز (تست شده) ---
CLEAN_IPS = [
    "www.visa.com", "www.udemy.com", "discord.com", "104.16.200.200", "162.159.135.42"
]

# --- منابع کانفیگ ---
URLS = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_configs():
    configs = []
    for url in URLS:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if len(line) > 10 and "vmess://" not in line: # وی‌مس را حذف کردم چون کند است
                        configs.append(line)
        except:
            pass
    return configs

def main():
    print("--- STARTING ---")
    raw_configs = get_configs()
    final_configs = []

    for conf in raw_configs:
        try:
            # استراتژی 1: ریلیتی (دست نزن)
            if "reality" in conf or "pbk=" in conf:
                final_configs.append(conf)
            
            # استراتژی 2: وی‌لس (تزریق آی‌پی)
            elif conf.startswith("vless://") and "type=ws" in conf:
                # چک کردن سلامت لینک
                if "@" in conf and ":" in conf:
                    ip = random.choice(CLEAN_IPS)
                    
                    # جدا کردن بخش‌های لینک
                    part1 = conf.split("@")[0]  # vless://uuid
                    part2 = conf.split("@")[1]  # address:port?params
                    
                    current_address = part2.split(":")[0]
                    rest_of_link = part2.split(":", 1)[1] # port?params
                    
                    # ساخت لینک جدید
                    new_link = f"{part1}@{ip}:{rest_of_link}"
                    
                    # اضافه کردن SNI اگر ندارد
                    if "sni=" not in new_link: 
                        if "?" in new_link: new_link += f"&sni={current_address}"
                        else: new_link += f"?sni={current_address}"
                    
                    # تغییر نام
                    if "#" in new_link:
                        new_link = new_link.split("#")[0] + "#🚀_MCI_Turbo"
                    else:
                        new_link += "#🚀_MCI_Turbo"

                    final_configs.append(new_link)
                else:
                    final_configs.append(conf)

            # استراتژی 3: بقیه (تروجان و ...)
            else:
                final_configs.append(conf)

        except:
            continue

    # اگر لیست خالی شد
    if not final_configs:
        final_configs = ["vless://uuid@127.0.0.1:443?type=ws&sni=google.com#ERROR"]

    # مخلوط کردن
    random.shuffle(final_configs)

    # ذخیره
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs[:100]))
    
    print("--- DONE ---")

if __name__ == "__main__":
    main()
