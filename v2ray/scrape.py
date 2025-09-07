import base64
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def fetch_text(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    try:
        if "://" not in text:
            text = base64.b64decode(text).decode('utf-8')
    except Exception:
        print(url + " base64 decode failed")
    if not text.endswith('\n'):
        text += '\n'
    print(text)
    return text


def save_text(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def v2rayshare():
    today = datetime.today()
    url = f"https://v2rayshare.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def aiboboxx():
    url = "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"
    text = fetch_text(url)
    return text


def miluonode():
    today = datetime.today()
    url = f"http://miluonode.cczzuu.top/node/{today.strftime('%Y%m%d')}-v2ray.txt"
    text = fetch_text(url)
    return text


def freeclash():
    today = datetime.today()
    url = f"https://free-clash-v2ray.github.io/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def freeclashnode():
    today = datetime.today()
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def vpnlogin():
    today = datetime.today()
    url = f"https://vpnlogin.github.io/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def v2rayshareorg():
    today = datetime.today()
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def v2rayclashfree():
    today = datetime.today()
    url = f"https://v2rayclashfree.com/feed/v2ray-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def nodefree():
    today = datetime.today()
    url = f"https://nodefree.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def nodeshare():
    today = datetime.today()
    url = f"https://a.nodeshare.xyz/uploads/{today.year}/{today.month:d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def cczzuu():
    today = datetime.today()
    url = f"http://bikfx.cczzuu.top/node/{today.strftime('%Y%m%d')}-v2ray.txt"
    text = fetch_text(url)
    return text


def oneclash():
    today = datetime.today()
    url = f"https://oneclash.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


def deduplicate(text):
    lines = text.split('\n')
    lines = [line.split('#')[0].strip() for line in lines if line.strip()]
    lines = sorted(set(lines))
    return '\n'.join(lines)


if __name__ == "__main__":
    text = ""
    text += miluonode()
    text += freeclash()
    text += freeclashnode()
    text += vpnlogin()
    text += v2rayshareorg()
    text += v2rayclashfree()
    text += nodefree()
    text += nodeshare()
    text += cczzuu()
    text += oneclash()
    text += v2rayshare()
    text += aiboboxx()
    text = deduplicate(text)
    text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    save_text(text, "v2ray.txt")
