import requests
import base64
import random
import re

# منابع اسکن شده و تمیز
CLEAN_IP_SOURCES = [
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_mci",
    "https://raw.githubusercontent.com/ircfspace/scanner/main/sub/sub_irancell"
]

# منابع کانفیگ
CONFIG_SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_clean_ips():
    print("--- Getting Clean IPs ---")
    ips = []
    for source in CLEAN_IP_SOURCES:
        try:
            resp = requests.get(source, timeout=10)
            if resp.status_code == 200:
                found = re.findall(r'[0-9]+(?:\.[0-9]+){3}', resp.text)
                ips.extend(found)
        except:
            pass
    return list(set(ips))

def get_configs():
    print("--- Getting Configs ---")
    configs = []
    for source in CONFIG_SOURCES:
        try:
            resp = requests.get(source, timeout=10)
            if resp.status_code == 200:
                configs.extend(resp.text.splitlines())
        except:
            pass
    return configs

def main():
    clean_ips = get_clean_ips()
    raw_configs = get_configs()
    
    if not clean_ips:
        clean_ips = ['104.16.200.200'] # آی پی زاپاس

    final_configs = []
    
    for conf in raw_configs:
        if "vless://" in conf and "reality" in conf:
            try:
                ip = random.choice(clean_ips)
                # جایگزینی ساده آی پی
                part1 = conf.split("@")[0]
                part2 = conf.split("@")[1]
                rest = part2.split("?")[1] if "?" in part2 else ""
                port = part2.split("?")[0].split(":")[1]
                host = part2.split("?")[0].split(":")[0]
                
                new_conf = f"{part1}@{ip}:{port}?{rest}"
                if "sni=" not in new_conf: new_conf += f"&sni={host}"
                new_conf += "#🚀_MCI_TURBO"
                
                final_configs.append(new_conf)
            except:
                continue

    # شافل و ذخیره
    random.shuffle(final_configs)
    top_100 = final_configs[:100]

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(top_100))

    print("Done!")

if __name__ == "__main__":
    main()
