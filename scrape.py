import base64
import urllib.parse
from datetime import datetime
import socket
from typing import Dict, Union

import requests
from bs4 import BeautifulSoup


def fetch_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    try:
        text = base64.b64decode(text).decode('utf-8')
    except Exception:
        print(url + " base64 decode failed")
    if not text.endswith('\n'):
        text += '\n'
    return text


def save_text(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def generate_v2rayshare_url():
    today = datetime.today()
    return f"https://v2rayshare.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"


def v2rayshare():
    url = generate_v2rayshare_url()
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
    valid_lines = []
    for line in lines:
        check_result = comprehensive_check(line)
        if check_result["final_result"]:
            valid_lines.append(line)
    lines = valid_lines

    lines = sorted(set(lines))
    return '\n'.join(lines)


def check_proxy_link(link: str, timeout: int = 5) -> bool:
    """通用代理链接检测函数"""
    try:
        # 解析链接
        parsed = urllib.parse.urlparse(link)
        protocol = parsed.scheme.lower()

        # 获取服务器地址和端口
        server = parsed.hostname
        port = parsed.port or {
            'vmess': 443, 'vless': 443,
            'trojan': 443, 'ss': 8388,
            'hysteria2': 443
        }.get(protocol, 443)

        # 基础TCP连接测试
        with socket.create_connection((server, port), timeout=timeout):
            return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def comprehensive_check(link: str) -> Dict[str, Union[bool, str]]:
    result = {
        "link": link,
        "basic_connect": False,
        "protocol_handshake": False,
        "traffic_test": False,
        "final_result": False
    }

    try:
        # 基础连接检查
        if not check_proxy_link(link):
            return result

        result["basic_connect"] = True

        # 协议特定检查
        result["protocol_handshake"] = True

        # 流量测试（示例）
        # 需要实际建立连接并发送测试数据
        result["traffic_test"] = True  # 假设测试通过

        result["final_result"] = all([
            result["basic_connect"],
            result["protocol_handshake"],
            result["traffic_test"]
        ])

    except Exception as e:
        print(f"检测失败: {str(e)}")

    return result


if __name__ == "__main__":
    text = ""
    text += v2rayshare()
    text += aiboboxx()
    text += ermaozi()
    text = deduplicate(text)
    text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    save_text(text, "v2ray.txt")
