# 中国银行外汇牌价(实时)
import requests
import time
from bs4 import BeautifulSoup
import pymysql

# 下载器
def download(url, headers):
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = 'utf-8'   # 处理乱码问题
    soup = BeautifulSoup(wb_data.text, 'lxml')
    time.sleep(2)  # 休眠两秒
    return soup

# 解析器
def parse(html):
    tag_table = html.find('table', attrs={'align': 'left', 'cellpadding': '0', 'width': '100%'})

    tr_list = tag_table.find_all('tr')

    for tr in tr_list[1:]:
        td_list = tr.find_all('td')
        result = []
        for td in td_list:
            result.append(td.get_text())
        for i in range(5):
            a = i+1
            if result[a] == '':
                result[a] = '0'
        operate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取操作时间
        result.append(operate_time)
        print(result)
        # 货币名称 现汇买入价 现钞买入价 现汇卖出价 现钞卖出价 中行折算价 发布日期 发布时间 操作时间
        # 写入数据库
        # mysql_insert(result)

# 写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='shares',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into ExchangeRate values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

# 爬虫主体
def exchange_rate():
    # 分页
    for i in range(1):
        tmp = ''
        if i:
            tmp = '_' + str(i)
        # 遍历统一资源定位符
        url = 'http://www.boc.cn/sourcedb/whpj/index{}.html'.format(tmp)

        # 消息头
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.boc.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2990.0 Safari/537.36'
        }

        # 调用下载器
        html = download(url, headers)
        # print(html)

        # 调用解析器
        parse(html)




# 主方法
if __name__ == '__main__':
    exchange_rate()