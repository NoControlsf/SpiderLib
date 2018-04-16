import pymysql
import requests
from bs4 import BeautifulSoup



#查询未爬取的链接
def mysql_search_links():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "SELECT company_link, area_name, bt_time FROM jsgs_link WHERE isget is null;"
    cur.execute(sql)
    search_list = []
    for r in cur:
        tmp = {}
        tmp['company_link'] = r['company_link']
        tmp['area_name'] = r['area_name']
        tmp['bt_time'] = r['bt_time']
        search_list.append(tmp)
    conn.commit()
    conn.close()
    #print(search_list)
    return search_list

# 正文写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into jsgs_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

def download(r):
    url = r['company_link']
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    parse(soup, r)


def parse(soup, r):
    table = soup.find('table', bordercolor='#AFD7F1')
    trs = table.find_all('tr')
    result = []
    for tr in trs:
        td = tr.find_all('td')[1].get_text().replace('\n', '').replace('\r', '').replace(' ', '')
        result.append(td)
    result.append(r['bt_time'])
    result.append('江苏省')
    if r['area_name'] == '江苏省':
        result.append('')
    else:
        result.append(r['area_name'])
    result.append(r['company_link'])
    # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人或者负责人姓名、性别、证件名称及号码
    # 负有直接责任的财务负责人姓名、性别、证件名称及号码  负有直接责任的中介机构信息及其从业人员信息
    # 案件性质  主要违法事实 相关法律依据及税务处理处罚情况 公布日期 所属省份 所属城市 链接
    print(result)
    mysql_insert(result)

def jsgs_detail_spider():
    search_list = mysql_search_links()
    if len(search_list) != 0:
        for r in search_list:
            download(r)



if __name__ == "__main__":
    jsgs_detail_spider()