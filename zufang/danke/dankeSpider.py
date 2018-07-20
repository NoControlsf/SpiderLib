import requests
from bs4 import BeautifulSoup

def download():
    url = 'https://www.dankegongyu.com/room/hz/d%E6%BB%A8%E6%B1%9F%E5%8C%BA.html?page=1'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=163b5d421ccb6-05f814913bbb15-454c062c-100200-163b5d421cd13f; LXB_REFER=www.baidu.com; _ga=GA1.2.1070348657.1527766512; _gid=GA1.2.92902096.1527766512; CNZZDATA1271579284=1476063934-1527759217-https%253A%252F%252Fwww.baidu.com%252F%7C1527780860; Hm_lvt_814ef98ed9fc41dfe57d70d8a496561d=1527763969,1527783123; RealyCookie=2018517147xervdkUfcf7ogE9yJsQxZumuoi8dzdA6TEfS_b3d1ca80f281df7ae28c2ea6a5f5c26b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218361296750%22%2C%22%24device_id%22%3A%22163b5d4214a8d-068a51f5ebc815-454c062c-1049088-163b5d4214c190%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fs%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%9B%8B%E5%A3%B3%E5%85%AC%E5%AF%93%22%2C%22platformType%22%3A%22PC%22%2C%22pid%22%3A%22dankegongyu_customer%22%2C%22cid%22%3A%22bj%22%2C%22ucid%22%3A%2218361296750%22%2C%22uuid%22%3A%2218361296750%22%2C%22ssid%22%3A%2218361296750%22%2C%22lmei%22%3A%22%22%2C%22android_id%22%3A%22%22%2C%22idfa%22%3A%22%22%2C%22idfv%22%3A%22%22%2C%22mac_id%22%3A%22%22%7D%2C%22first_id%22%3A%22163b5d4214a8d-068a51f5ebc815-454c062c-1049088-163b5d4214c190%22%7D; Hm_lpvt_814ef98ed9fc41dfe57d70d8a496561d=1527783915; XSRF-TOKEN=eyJpdiI6Inp3eXVCUG80ZUNcLzJxWHVxRHNFTTNnPT0iLCJ2YWx1ZSI6Im5qTjR2YmVnSWh5ZkZPejN5NzNqblVka0JwcitxTUVaSTlQYVpEZmdaeklXUmRZZHI2Q1ZYZjBETWRcLzJvNFZVSnNHeEdvQjM4MTBjUkd4NEh1MHQ1UT09IiwibWFjIjoiNDZkMGVmNDkxM2Q2NDZjNjk1M2Y2YjJhYTc2NWJhYzdkODIwNTNiYmJhNTc5NzA3N2JlYTg0NTJhNGJiMzZhYyJ9; session=eyJpdiI6IkZRXC9FaEwrR2pvcUU3Z1RFcVczVHZnPT0iLCJ2YWx1ZSI6Im0rQTFIZnl6XC9KMXVCZGswRkZyU2h6emRpTXFLbnNRRUFDSFZlbGlVVGxQZ1V0MlNxM3JlMzQzSk5rbmRVSmFUVURPTjNqelV2b1ZjeVdzNEZsR21vUT09IiwibWFjIjoiYzM3NzkzZGRhZjhlMTFlNWQ4YzkyYzViODM4YjljMzhjODFjNTFlMGZjYTg4M2RiZGIxY2NmMTQzOTdlYTg0MSJ9',
        'Host': 'www.dankegongyu.com',
        #'Referer': 'https://www.dankegongyu.com/room/hz/d%E6%BB%A8%E6%B1%9F%E5%8C%BA.html?page=2',
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml').find('div', class_='r_ls_box')
    print(soup)


if __name__ == "__main__":
    download()