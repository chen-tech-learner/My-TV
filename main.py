import requests
import re

# 可以放多个m3u地址，随便加，最后一条不要逗号
SOURCE_URLS = [
    "https://raw.githubusercontent.com/vbskycn/iptv/refs/heads/master/tv/iptv4.m3u",
    "https://gh-proxy.com/https://raw.githubusercontent.com/yoursmile66/TVBox/refs/heads/main/live.txt",
    "https://gh-proxy.com/https://raw.githubusercontent.com/fleung49/star/refs/heads/main/mit"
]

OUTPUT_FILE = "my_tv.m3u"

# 超时，检测链接通不通
CHECK_TIMEOUT = 8

def check_url_ok(url):
    try:
        r = requests.head(url, timeout=CHECK_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False


def fetch_one(url):
    try:
        resp = requests.get(url, timeout=30)
        resp.encoding = "utf‑8"
        return resp.text
    except Exception as e:
        print(f"获取失败 {url} : {e}")
        return ""


def main():
    all_lines = []
    for src in SOURCE_URLS:
        text = fetch_one(src)
        if not text:
            continue
        lines = text.splitlines()
        all_lines.extend(lines)

    out = []
    cache_url = None
    for line in all_lines:
        line = line.rstrip("\n\r")
        if line.startswith("#EXTINF"):
            out.append(line)
        elif line.startswith("http"):
            cache_url = line
            if check_url_ok(cache_url):
                out.append(cache_url)
            else:
                print(f"丢弃死链：{cache_url}")

    with open(OUTPUT_FILE, "w", encoding="utf‑8") as f:
        f.write("\n".join(out))
    print(f"已保存到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
