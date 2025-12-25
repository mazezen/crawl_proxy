"""
定时爬取 HTTP | HTTPS | SOCKS4 | SOCKS5 IP
IP 保存到 *.dat 文件中
"""

from crawl import fetch, crawl_proxy_list
from parse import parse

if __name__ == '__main__':
    env = parse()
    fetch(env)
    crawl_proxy_list(env)