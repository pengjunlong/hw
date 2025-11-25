import base64
import json
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def fetch_text(url):
    try:
        logging.info(f"Fetching from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        try:
            if "://" not in text:
                text = base64.b64decode(text).decode('utf-8')
        except Exception as e:
            logging.warning(f"{url} base64 decode failed: {str(e)}")
        if not text.endswith('\n'):
            text += '\n'
        logging.info(f"Number of lines in text: {len(text.splitlines())}")
        return text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {str(e)}")
        return ""
    except Exception as e:
        logging.error(f"Unexpected error processing {url}: {str(e)}")
        return ""


def safe_fetch(func):
    """装饰器，用于安全地获取文本，避免因异常导致程序终止"""
    def wrapper():
        try:
            return func()
        except Exception as e:
            source_name = func.__name__
            logging.error(f"Error in {source_name}: {str(e)}")
            return ""
    return wrapper


def save_text(text, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        logging.info(f"Successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving to {filename}: {str(e)}")


@safe_fetch
def v2rayshare():
    today = datetime.today()
    url = f"https://v2rayshare.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def aiboboxx():
    url = "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"
    text = fetch_text(url)
    return text


@safe_fetch
def miluonode():
    today = datetime.today()
    url = f"http://miluonode.cczzuu.top/node/{today.strftime('%Y%m%d')}-v2ray.txt"
    text = fetch_text(url)
    return text





@safe_fetch
def v2rayshareorg():
    today = datetime.today()
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/1-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/2-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/3-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.v2rayshare.org/uploads/{today.year}/{today.month:02d}/4-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    return text


@safe_fetch
def v2rayclashfree():
    today = datetime.today()
    url = f"https://v2rayclashfree.com/feed/v2ray-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def nodefree():
    today = datetime.today()
    url = f"https://nodefree.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text

@safe_fetch
def cczzuu():
    today = datetime.today()
    url = f"http://bikfx.cczzuu.top/node/{today.strftime('%Y%m%d')}-v2ray.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def jichangx():
    today = datetime.today()
    url = f"https://jichangx.com/nodes/v2ray-{today.strftime('%Y%m%d')}-01"
    text = fetch_text(url)
    return text


@safe_fetch
def oneclash():
    today = datetime.today()
    url = f"https://oneclash.githubrowcontent.com/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text



@safe_fetch
def v2rayfree():
    url = f"https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v2"
    text = fetch_text(url)
    return text


@safe_fetch
def ebrasha():
    url = f"https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/all_extracted_configs.txt"
    text = fetch_text(url)
    return text


def add_source_prefix(text, source_name):
    """
    为各种协议的链接添加 source 前缀到备注信息
    支持的协议：vmess://, vless://, shadowsocks://, ss://, trojan://
    对于 vmess:// 协议，会解码 JSON 并修改 ps 字段
    对于其他协议，会在 URL 备注中添加前缀
    """
    try:
        lines = text.split('\n')
        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            original_line = line

            # 处理 vmess:// 协议 - 需要解码 JSON 修改 ps 字段
            if line.startswith('vmess://'):
                line = process_vmess_link(line, source_name)
            # 处理其他协议 - 在 URL 备注中添加前缀
            elif line.startswith(('vless://', 'shadowsocks://', 'ss://', 'trojan://')):
                # 分离链接和备注
                if '#' in line:
                    # 已经有备注，替换或添加前缀
                    link_part, comment = line.split('#', 1)
                    new_comment = f"[{source_name}] {comment}"
                    line = f"{link_part}#{new_comment}"
                else:
                    # 没有备注，添加新的备注
                    line = f"{line}#[{source_name}]"

            processed_lines.append(line)

        return '\n'.join(processed_lines)
    except Exception as e:
        logging.error(f"Error in add_source_prefix for {source_name}: {str(e)}")
        return text


def process_vmess_link(vmess_link, source_name):
    """
    处理 vmess:// 链接，解码 JSON 并修改 ps 字段
    """
    try:
        # 分离 base64 部分和 URL 备注
        if '#' in vmess_link:
            base64_part, url_comment = vmess_link.split('#', 1)
            base64_part = base64_part[8:]  # 去掉 'vmess://'
        else:
            base64_part = vmess_link[8:]  # 去掉 'vmess://'
            url_comment = None

        # 解码 base64
        try:
            decoded_json = base64.b64decode(base64_part).decode('utf-8')
            config = json.loads(decoded_json)

            # 修改 ps 字段
            original_ps = config.get('ps', '')
            if original_ps:
                config['ps'] = f"[{source_name}] {original_ps}"
            else:
                config['ps'] = f"[{source_name}]"

            # 重新编码为 base64
            new_json = json.dumps(config, separators=(',', ':'), ensure_ascii=False)
            new_base64 = base64.b64encode(new_json.encode('utf-8')).decode('utf-8')

            # 重新构建链接
            new_link = f"vmess://{new_base64}"
            if url_comment:
                new_link += f"#{url_comment}"

            return new_link

        except Exception as e:
            logging.warning(f"Failed to decode/encode vmess JSON for {source_name}: {e}")
            # 如果 JSON 处理失败，回退到简单的 URL 备注方式
            if url_comment:
                return f"{vmess_link.split('#')[0]}#[{source_name}] {url_comment}"
            else:
                return f"{vmess_link}#[{source_name}]"

    except Exception as e:
        logging.error(f"Error processing vmess link for {source_name}: {e}")
        return vmess_link


def deduplicate(text):
    try:
        lines = text.split('\n')
        lines = [line.split('#')[0].strip() for line in lines if line.strip()]
        lines = sorted(set(lines))
        return '\n'.join(lines)
    except Exception as e:
        logging.error(f"Error in deduplicate: {str(e)}")
        return text


if __name__ == "__main__":
    try:
        logging.info("Starting v2ray scraping process")
        text = ""

        # 定义所有源函数
        sources = [
            miluonode, v2rayshareorg, v2rayclashfree, nodefree, cczzuu,
            oneclash, v2rayshare, aiboboxx, v2rayfree,
            jichangx,
        ]

        # 依次调用每个源函数
        for source in sources:
            source_name = source.__name__
            logging.info(f"Processing source: {source_name}")
            result = source()
            if result:
                # 为当前源的数据添加 source 前缀
                prefixed_result = add_source_prefix(result, source_name)
                text += prefixed_result
                logging.info(f"Successfully fetched and prefixed data from {source_name}")
            else:
                logging.warning(f"No data fetched from {source_name}")

        if not text:
            logging.error("No data fetched from any source")
            exit(1)

        logging.info("Deduplicating data")
        text = deduplicate(text)
        logging.info(f"text: {text}")
        logging.info(f"Number of lines in deduplicated text: {len(text.splitlines())}")

        logging.info("Encoding data to base64")
        text = base64.b64encode(text.encode('utf-8')).decode('utf-8')

        logging.info("Saving data to file")
        save_text(text, "v2ray.txt")

        logging.info("Process completed successfully")
    except Exception as e:
        logging.critical(f"Critical error in main process: {str(e)}")
