import requests
import concurrent.futures
import time
from collections import defaultdict


proxies = [
    '192.111.135.18:18301',
    '3.130.65.162:3128',
    '36.150.4.6:12798',
    '101.200.158.109:9200',
    '47.122.31.238:8081',
    '47.92.152.43:7890',
    '46.105.105.223:5589',
    '192.252.215.2:4145',
    '192.111.139.165:4145',
    '3.130.65.162:80',
    '183.240.46.42:443',
    '18.169.83.87:3128',
    '139.99.9.218:5927',
    '13.246.209.48:1080',
    '47.91.115.179:4145',
    '171.38.145.185:8085',
    '54.67.125.45:3128',
    '36.92.28.34:8080',
    '8.130.90.177:6379',
    '39.102.214.208:8008',
    '103.189.218.85:6969',
    '47.92.194.235:8118',
    '47.104.27.165:80',
    '47.122.5.165:8080',
    '120.25.189.254:8081',
    '217.27.149.249:3128',
    '31.220.15.234:80',
    '51.17.58.162:3128',
    '44.226.167.102:3128',
    '103.214.102.43:8083',
    '50.63.12.101:61120',
    '47.237.107.41:8081',
    '72.205.54.36:4145',
    '3.126.147.182:3128',
    '54.233.119.172:3128',
    '181.57.184.46:1080',
    '39.102.208.149:80',
    '47.114.165.250:8222',
    '3.90.100.12:3128',
    '20.205.61.143:8123',
    '121.227.146.81:8089',
    '142.54.237.38:4145',
    '177.104.87.23:5678',
    '47.237.92.86:5060',
    '47.97.24.122:8222',
    '47.119.20.8:9080',
    '35.178.104.4:1080',
    '132.148.167.243:46843',
    '52.26.114.229:1080',
    '39.101.65.228:41890',
    '39.104.69.76:8800',
    '174.75.211.222:4145',
    '199.116.112.6:4145',
    '98.181.137.80:4145',
    '174.77.111.197:4145',
    '47.91.120.190:80',
    '8.211.195.173:8080',
    '45.12.132.28:50691',
    '188.165.133.80:30863',
    '203.95.198.180:8080',
    '195.158.8.123:3128',
    '39.102.211.162:8080',
    '20.204.43.57:80',
    '115.127.139.90:58080',
    '8.130.74.114:80',
    '199.102.104.70:4145',
    '117.50.205.222:8888',
    '139.9.62.87:8080',
    '104.200.152.30:4145',
    '47.122.65.32:3128',
    '192.95.33.162:36749',
    '64.202.184.249:32102',
    '8.148.23.202:4000',
    '47.122.31.238:1900',
    '172.235.29.87:8080',
    '39.101.65.228:9992',
    '139.129.202.244:80',
    '44.195.247.145:80',
    '132.148.167.243:16444',
    '44.218.183.55:80',
    '51.77.170.182:8080',
    '103.250.128.1:8082',
    '54.212.162.236:3128',
    '213.165.185.211:4153',
    '72.10.160.170:8849',
    '47.91.115.179:9098',
    '47.100.223.33:12080',
    '47.250.51.110:8443',
    '3.141.217.225:3128',
    '199.229.254.129:4145',
    '68.71.254.6:4145',
    '8.137.13.191:8443',
    '101.132.222.120:80',
    '98.191.0.47:4145',
    '64.202.184.249:7652',
    '47.104.27.249:8081',
    '47.251.87.199:8080',
    '185.95.0.197:55284',
    '45.92.177.60:8080',
    '103.149.177.204:3128'
]


def try_protocol(proxy, protocol):
    protocol_variants = {
        'socks4': ['socks4', 'socks4a'],
        'socks5': ['socks5', 'socks5h'],
        'http': ['http'],
        'https': ['https']
    }.get(protocol, [protocol])

    min_delay = None
    test_urls = [
        'https://httpbin.org/ip',
        # 'https://www.youtube.com',
        'https://www.baidu.com',
        'https://cn.bing.com'
    ]

    for variant in protocol_variants:
        proxies_config = {
            'http': f'{variant}://{proxy}',
            'https': f'{variant}://{proxy}'
        }

        for test_url in test_urls:
            try:
                start_time = time.time()
                response = requests.get(test_url,
                                      proxies=proxies_config,
                                      timeout=5,
                                      headers={'User-Agent': 'Mozilla/5.0'})

                if 'httpbin.org' in test_url:
                    if response.status_code == 200 and 'origin' in response.json():
                        delay = (time.time() - start_time) * 1000
                        if not min_delay or delay < min_delay:
                            min_delay = delay
                        break
                else:
                    if response.status_code == 200:
                        delay = (time.time() - start_time) * 1000
                        if not min_delay or delay < min_delay:
                            min_delay = delay
                        break

            except Exception as e:
                continue

    return (proxy, protocol, min_delay)


def main():
    results = defaultdict(dict)
    protocols = ['http', 'https', 'socks4', 'socks5']

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(try_protocol, proxy, protocol)
                   for proxy in proxies
                   for protocol in protocols]

        for future in concurrent.futures.as_completed(futures):
            try:
                proxy, protocol, delay = future.result()
                if delay:
                    if protocol in results[proxy]:
                        if delay < results[proxy][protocol]:
                            results[proxy][protocol] = delay
                    else:
                        results[proxy][protocol] = delay
            except Exception as e:
                print(f"测试出错: {e}")

    for proxy in proxies:
        print(f"\n代理：{proxy}")
        if proxy in results and results[proxy]:
            for protocol in protocols:
                if delay := results[proxy].get(protocol):
                    print(f"  ✅ {protocol.upper()} 延迟：{delay:.2f}ms")
                else:
                    print(f"  ❌ {protocol.upper()} 不可用")
        else:
            print("  ❌ 所有协议均不可用")


if __name__ == "__main__":
    main()
