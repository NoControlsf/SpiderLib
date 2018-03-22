import requests
from bs4 import BeautifulSoup


def download():
    pass

def parse():
    pass


def baidu_zhishu():
    url = 'http://index.baidu.com/?tpl=trend&word=python'
    wb_data = requests.get(url)
    wb_data.encoding = 'gbk'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup)

if __name__ == "__main__":
    baidu_zhishu()