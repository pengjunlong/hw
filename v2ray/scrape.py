import base64
import urllib.parse
from datetime import datetime
import socket
from typing import Dict, Union

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


def ermaozi():
    url = "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt"
    text = fetch_text(url)
    return text


def deduplicate(text):
    lines = text.split('\n')
    lines = [line.split('#')[0].strip() for line in lines if line.strip()]
    lines = sorted(set(lines))
    return '\n'.join(lines)


if __name__ == "__main__":
    text = ""
    text += v2rayshare()
    text += aiboboxx()
    text += ermaozi()
    text = deduplicate(text)
    print(text)
    text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    save_text(text, "result.txt")
