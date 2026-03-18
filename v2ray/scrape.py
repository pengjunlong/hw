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
    """模拟浏览器请求，避免被网站拒绝"""
    try:
        logging.info(f"Fetching from: {url}")

        # 创建一个session，保持cookie
        session = requests.Session()

        # 浏览器请求头
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }

        # 初始cookies
        cookies = {
            '_ga': 'GA1.1.1295861470.1772533462',
            '_ga_YPV3FLCLJZ': 'GS2.1.s1772596569$o2$g1$t1772596576$j53$l0$h0'
        }

        # 使用session发送请求
        response = session.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=30,
            allow_redirects=True
        )

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

        # 关闭session
        session.close()

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
def v2rayfree():
    today = datetime.today()
    url = f"https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v{today.strftime('%Y%m%d')}1"
    text = fetch_text(url)
    url = f"https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v{today.strftime('%Y%m%d')}2"
    text += fetch_text(url)
    return text


@safe_fetch
def miluonode():
    today = datetime.today()
    url = f"http://miluonode.cczzuu.top/node/{today.strftime('%Y%m%d')}-v2ray.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def clashgithub():
    today = datetime.today()
    url = f"https://clashgithub.com/wp-content/uploads/rss/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def oneclash():
    today = datetime.today()
    url = f"https://oss.oneclash.cc/{today.year}/{today.month:02d}/{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    return text


@safe_fetch
def mibei():
    """从米呗网站获取 v2ray 节点"""
    try:
        import re
        today_str = datetime.today().strftime('%Y%m%d')
        logging.info(f"Starting mibei scraping for date: {today_str}")

        # 创建session用于保持cookie
        session = requests.Session()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }

        # 步骤1: 访问主页，获取包含今天日期的链接
        logging.info(f"Step 1: Fetching main page: https://www.mibei77.com/")
        response = session.get('https://www.mibei77.com/', headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 查找所有链接
        article_url = None
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 检查是否包含今天日期且以 "-v2rayclash-vpn.html" 结尾
            if today_str in href and href.endswith('-v2rayclash-vpn.html'):
                article_url = href if href.startswith('http') else f"https://www.mibei77.com/{href}"
                logging.info(f"Found article URL: {article_url}")
                break

        if not article_url:
            logging.warning("No matching article found for today's date")
            session.close()
            return ""

        # 步骤2: 访问文章页，获取 .txt 文件链接（从文本中提取）
        logging.info(f"Step 2: Fetching article page: {article_url}")
        response = session.get(article_url, headers=headers, timeout=30)
        response.raise_for_status()

        # 使用正则表达式从文本中提取 https://mm.mibei77.com/ 开头且以 .txt 结尾的链接
        text = response.text
        txt_url_pattern = r'https://mm\.mibei77\.com/[^\s]+\.txt'
        txt_urls = re.findall(txt_url_pattern, text)

        if not txt_urls:
            logging.warning("No txt file link found in article text")
            session.close()
            return ""

        # 取第一个匹配的链接
        txt_url = txt_urls[0]
        logging.info(f"Found txt URL: {txt_url}")

        # 步骤3: 访问 .txt 文件获取内容
        logging.info(f"Step 3: Fetching txt file: {txt_url}")
        response = session.get(txt_url, headers=headers, timeout=30)
        response.raise_for_status()

        # 尝试解码 base64（如果需要）
        text = response.text
        try:
            if "://" not in text:
                text = base64.b64decode(text).decode('utf-8')
        except Exception as e:
            logging.warning(f"base64 decode failed: {str(e)}")

        if not text.endswith('\n'):
            text += '\n'

        logging.info(f"Successfully fetched mibei data, lines: {len(text.splitlines())}")

        session.close()
        return text

    except Exception as e:
        logging.error(f"Error in mibei: {str(e)}")
        return ""


@safe_fetch
def yoyapai():
    today = datetime.today()
    url = f"https://yoyapai.com/mianfeijiedian/{today.strftime('%Y%m%d')}-ssr-v2rayvpnjiedian-yoyapai.com.txt"
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
def freeclashnode():
    today = datetime.today()
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/0-{today.strftime('%Y%m%d')}.txt"
    text = fetch_text(url)
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/1-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/2-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/3-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
    url = f"https://node.freeclashnode.com/uploads/{today.year}/{today.month:02d}/4-{today.strftime('%Y%m%d')}.txt"
    text += fetch_text(url)
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
            elif line.startswith(('vless://', 'shadowsocks://', 'ss://', 'trojan://', 'hysteria2://')):
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
    """
    基于链接核心部分进行去重，保留第一个遇到的版本
    对于 vmess:// 协议，需要解码后比较（不包含 ps 字段）
    对于其他协议，比较 # 之前的核心部分
    """
    try:
        lines = text.split('\n')
        logging.info(f"before deduplicate, Number of lines in text: {len(lines)}")
        seen_links = {}  # 存储核心链接到完整链接的映射

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 提取链接核心部分用于去重
            core_link = extract_core_link(line)

            # 如果这个核心链接还没见过，就记录下来
            if core_link and core_link not in seen_links:
                seen_links[core_link] = line

        # 返回去重后的链接，按协议类型排序
        result = sort_by_protocol(list(seen_links.values()))
        logging.info(f"after deduplicate, Number of lines in text: {len(result)}")
        return '\n'.join(result)
    except Exception as e:
        logging.error(f"Error in deduplicate: {str(e)}")
        return text


def get_protocol_type(link):
    """
    获取链接的协议类型，用于排序
    返回协议的优先级数字（数字越小排序越靠前）
    """
    protocol_order = {
        'vmess://': 0,
        'vless://': 1,
        'trojan://': 2,
        'shadowsocks://': 3,
        'ss://': 4,
        'hysteria2://': 5,
    }

    for protocol, order in protocol_order.items():
        if link.startswith(protocol):
            return order

    # 未知协议排在最后
    return 999


def sort_by_protocol(links):
    """
    按协议类型对链接进行排序
    排序顺序：vmess -> vless -> trojan -> shadowsocks -> ss -> hysteria2 -> 其他
    """
    try:
        # 使用协议类型作为主排序键，链接本身作为次排序键（确保稳定性）
        return sorted(links, key=lambda link: (get_protocol_type(link), link))
    except Exception as e:
        logging.error(f"Error in sort_by_protocol: {e}")
        # 如果排序失败，返回原始顺序
        return links


def extract_core_link(link):
    """
    提取链接的核心部分用于去重比较
    对于 vmess://，返回解码后去掉 ps 字段的 JSON
    对于其他协议，返回 # 之前的核心部分
    """
    try:
        if link.startswith('vmess://'):
            # 分离 base64 部分和 URL 备注
            if '#' in link:
                base64_part = link.split('#')[0][8:]
            else:
                base64_part = link[8:]

            # 解码 JSON 并移除 ps 字段
            try:
                decoded_json = base64.b64decode(base64_part).decode('utf-8')
                config = json.loads(decoded_json)

                # 创建去掉 ps 字段的配置
                config_without_ps = {k: v for k, v in config.items() if k != 'ps'}

                # 重新编码为字符串（用于比较）
                core_json = json.dumps(config_without_ps, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
                return f"vmess_core:{core_json}"
            except Exception as e:
                logging.warning(f"Failed to decode vmess for deduplication: {e}")
                # 回退到原始链接
                return link.split('#')[0] if '#' in link else link

        else:
            # 对于其他协议，返回 # 之前的核心部分
            if '#' in link:
                return link.split('#')[0]
            else:
                return link

    except Exception as e:
        logging.error(f"Error extracting core link: {e}")
        return link


if __name__ == "__main__":
    try:
        logging.info("Starting v2ray scraping process")
        text = ""

        # 定义所有源函数及其名称
        sources = [
            (miluonode, "miluonode"),
            (mibei, "mibei"),
            (cczzuu, "cczzuu"),
            (jichangx, "jichangx"),
            (yoyapai, "yoyapai"),
            (v2rayfree, "v2rayfree"),
            (clashgithub, "clashgithub"),
            (freeclashnode, "freeclashnode"),
            (v2rayshareorg, "v2rayshareorg"),
        ]

        # 依次调用每个源函数
        for source_func, source_name in sources:
            logging.info(f"Processing source: {source_name}")
            result = source_func()
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
        # logging.info(f"text: {text}")
        logging.info(f"Number of lines in deduplicated text: {len(text.splitlines())}")

        logging.info("Encoding data to base64")
        text = base64.b64encode(text.encode('utf-8')).decode('utf-8')

        logging.info("Saving data to file")
        save_text(text, "v2ray.txt")

        logging.info("Process completed successfully")
    except Exception as e:
        logging.critical(f"Critical error in main process: {str(e)}")
