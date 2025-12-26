import requests
import time
from bs4 import BeautifulSoup
from tools import exec_js


def fetch(env):
    filePath = "./data.dat"

    with open(file=filePath, mode='w') as file:
        pass

    http_proxies = []
    https_proxies = []
    socks4_proxies = []
    socks5_proxies = []

    try:
        response = requests.get(url=env.get('geonode_url'), timeout=10)
        if response.status_code != 200:
            print("[-] 获取代理 失败" + str(response.status_code))
            return

        res_json = response.json()
        # print(f"res_json: {res_json}")

        for row in res_json['data']:
            ip = row["ip"].strip()
            port = row["port"]
            if "socks5" in row["protocols"]:
                d = f"socks5://{ip}:{port}"
                socks5_proxies.append(d)
            if "socks4" in row["protocols"]:
                d = f"socks4://{ip}:{port}"
                socks4_proxies.append(d)
            if "http" in row["protocols"]:
                d = f"http://{ip}:{port}"
                http_proxies.append(d)
            if "https" in row["protocols"]:
                d = f"https://{ip}:{port}"
                https_proxies.append(d)

        # print("[-] 结束本次获取代理IP ")
        # 写入文件
        with open(filePath, "a") as file:
            for v in socks5_proxies: 
                file.write(v + "\n")
            for v in socks4_proxies: 
                file.write(v + "\n")
            for v in https_proxies: 
                file.write(v + "\n")
            for v in http_proxies: 
                file.write(v + "\n")

    except requests.exceptions.ConnectionError as e:
        print("[-] 获取代理失败 " + str(e))
   
def crawl_proxy_list(env):

    filepath = "./data2.dat"

    with open(filepath, 'w') as file:
        pass

    try:
        url = env.get('proxy_list_url')+"socks5"
        response_socks5 = requests.get(url=url)
        if response_socks5.status_code != 200:
            print("[-] 获取 proxy_list 代理 失败" + str(response_socks5.status_code))
            return
        
        if response_socks5.headers.get("Content-Type") == "text/plain; charset=utf-8":
            with open(filepath, 'a') as file:
                file.write("========================= socks5 =========================\n")
                file.write(response_socks5.text)
                file.write("\n\n")

        time.sleep(5)
        url_socks4 = env.get('proxy_list_url')+"socks4"
        response_socks4 = requests.get(url=url_socks4)
        if response_socks4.status_code != 200:
            print("[-] 获取 proxy_list socks4 代理 失败" + str(response_socks4.status_code))
            return

        if response_socks4.headers.get("Content-Type") == "text/plain; charset=utf-8":
            with open(filepath, 'a') as file:
                file.write("========================= socks4 =========================\n")
                file.write(response_socks4.text)
                file.write("\n\n")

        time.sleep(5)
        url_https = env.get("proxy_list_url")+"https"
        response_https = requests.get(url=url_https)
        if response_https.status_code != 200:
            print("[-] 获取 proxy_list https 代理 失败" + str(response_https.status_code))
            return
        if response_https.headers.get("Content-Type") == "text/plain; charset=utf-8":
            with open(filepath, 'a') as file:
                file.write("========================= https =========================\n")
                file.write(response_https.text)
                file.write("\n\n")

        time.sleep(5)
        url_http = env.get("proxy_list_url")+"http"
        response_http = requests.get(url=url_http)
        if response_http.status_code != 200:
            print("[-] 获取 proxy_list https 代理 失败" + str(response_http.status_code))
            return
        if response_http.headers.get("Content-Type") == "text/plain; charset=utf-8":
            with open(filepath, 'a') as file:
                file.write("========================= http =========================\n")
                file.write(response_http.text)
            


    except requests.exceptions.ConnectionError as e:
        print("[-] 获取代理失败 " + str(e))

def crawl_free_proxy_list(env):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(
            url=env.get('free_proxy_list_url'),
            headers=headers,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        print(f"[-] 获取 free_proxy_list proxy 代理失败: {e}")
        return None

    if response.headers.get("Content-Type") == "text/html; charset=utf-8":
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())

        lines = []
        for row in soup.find("table").find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) > 7:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                code = cols[2].text.strip()
                country = cols[3].text.strip()
                https = cols[6].text.strip()
                line = f"ip: {ip}  port: {port}  code: {code}  country: {country}"
                if https == "yes":
                    lines.append(line)

        with open('./data3.dat', 'w') as file:
            pass

        with open('./data3.dat', 'a') as file:
            for l in lines:
                file.write(l+"\n")

def crawl_proxy_nova(env):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        response = requests.get(url=env.get('proxy_nova_url'), headers=headers, timeout=10)

        if response.headers.get('Content-Type') == "text/html; charset=UTF-8":
            soup = BeautifulSoup(response.text, "html.parser")

            lines = []
            for row in soup.find("table").find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) == 7:
                    ip = cols[0].select("script")[0].text.split('document.write(',maxsplit=1)[1][:-1]   
                    ip = exec_js(ip) 
                    port = cols[1].text.strip()
                    speed = cols[3].select("small")[0].text
                    country = cols[5].select("a")[0].text.split("-")[0]   
                    line = f"ip: {ip}  port: {port}  speed: {speed}  country: {country}"
                    lines.append(line.strip())

            filepath = "./data4.dat"

            with open(filepath, 'w') as file:
                pass

            with open(filepath, 'a') as file:
                for line in lines:
                    file.write(line+"\n")

    except requests.exceptions.ConnectionError as e:
        print(f"[-] 获取 free_proxy_list proxy 代理失败: {e}")
        return None