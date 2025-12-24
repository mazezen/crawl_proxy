import requests
import time

def fetch():

    filePath = "./data.dat"

    with open(file=filePath, mode='w') as file:
        pass

    http_proxies = []
    https_proxies = []
    socks4_proxies = []
    socks5_proxies = []


    url = f"https://proxylist.geonode.com/api/proxy-list?limit=500&page={1}&sort_by=lastChecked&sort_type=desc"
    try:
        response = requests.get(url=url, timeout=10)
        if response.status_code != 200:
            print("[-] 获取代理 失败" + str(response.status_code))

        res_json = response.json()
        print(f"res_json: {res_json}")

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

        print("[-] 结束本次获取代理IP ")
        # 写入文件
        with open(filePath, "a") as file:
            # 按类别写入代理
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
    
    
   