import requests
import os
from urllib.parse import urlparse

# 尝试访问指定网址并返回有效性
def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if "动漫剧情" in response.text:
                print(f"✅ Valid domain found with matching content: {url}")
                return url
            else:
                print(f"❌ Invalid domain (content mismatch): {url}")
                return None
        else:
            print(f"❌ Invalid domain (Status code: {response.status_code}): {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Failed to access {url}: {e}")
        return None


def main():
    base_url_template = "http://{domain}/vodtype/9-2.html"
    valid_links = []

    # 这里可以调整范围，比如 8000-8099
    for i in range(8160, 8199):
        domain = f"{i}ck.cc"
        url_to_test = base_url_template.format(domain=domain)
        print(f"Testing URL: {url_to_test}")

        valid_url = check_url(url_to_test)
        if valid_url:
            domain_only = urlparse(valid_url).scheme + "://" + urlparse(valid_url).hostname
            valid_links.append(domain_only)

    if valid_links:
        updated_links = list(set(valid_links))  # 去重
        file_path = "JB/valid_links2.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(updated_links))
        print(f"✅ 有效域名已写入 {file_path}")
    else:
        print("⚠️ 没有找到有效的链接。")


if __name__ == "__main__":
    main()
