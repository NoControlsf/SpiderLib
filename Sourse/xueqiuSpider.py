import json

import requests
import time
from bs4 import BeautifulSoup

def download():
    for i in range(1, 11):
        time.sleep(5)
        url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id=9742512811'.format(i)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'aliyungf_tc=AQAAAFCdGzpLKAIAvg3XOqymKtViXCxk; xq_a_token=19f5e0044f535b6b1446bb8ae1da980a48bbe850; xq_a_token.sig=aaTVFAX9sVcWtOiu-5L8dL-p40k; xq_r_token=6d30415b5f855c12fd74c6e2fb7662ea40272056; xq_r_token.sig=rEvIjgpbifr6Q_Cxwx7bjvarJG0; u=481521610230716; device_id=8ff7429b96f207f84ebc2dd00dc3753e; __utmt=1; __utma=1.1429132228.1521610237.1521610237.1521613096.2; __utmb=1.1.10.1521613096; __utmc=1; __utmz=1.1521610237.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1521610237; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1521613096',
            'Host': 'xueqiu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        wb_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        parse(soup)

def parse(soup):
    json_str = soup.find('p').get_text()
    #res_json = json.loads(json_str)
    print(json_str)


if __name__ == "__main__":
    download()