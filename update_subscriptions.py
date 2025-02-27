import base64
import json
import requests

# لیست ساب لینک‌ها که باید بررسی شوند
SUB_LINKS = [
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/networks/grpc",
    "https://example.com/sub2"
]

OUTPUT_FILE = "merged_subscription.txt"

def decode_v2ray_sub(subscription_data):
    """دیکد کردن ساب لینک و استخراج سرورها"""
    decoded_data = base64.b64decode(subscription_data).decode()
    servers = [line for line in decoded_data.split("\n") if line]
    return servers

def fetch_and_merge_subscriptions(sub_links):
    """دریافت و ترکیب سرورهای مختلف از ساب لینک‌ها"""
    all_servers = []
    
    for link in sub_links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                servers = decode_v2ray_sub(response.text)
                all_servers.extend(servers)
            else:
                print(f"مشکل در دریافت {link}")
        except Exception as e:
            print(f"خطا در پردازش {link}: {e}")

    return all_servers

def save_subscription_file(servers, output_file):
    """ذخیره ساب لینک مادر به صورت Base64"""
    merged_data = "\n".join(servers)
    encoded_data = base64.b64encode(merged_data.encode()).decode()
    
    with open(output_file, "w") as f:
        f.write(encoded_data)
    
    print(f"فایل ساب لینک جدید در {output_file} ذخیره شد.")

if __name__ == "__main__":
    merged_servers = fetch_and_merge_subscriptions(SUB_LINKS)
    save_subscription_file(merged_servers, OUTPUT_FILE)

