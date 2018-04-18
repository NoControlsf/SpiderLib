import pymysql
import requests
import time
from bs4 import BeautifulSoup

def download():
    url = 'http://www.zj-l-tax.gov.cn/col/col1229555/index.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'zh_choose=n; yfx_c_g_u_id_10003730=_ck18041616333116811896319053781; yfx_f_l_v_t_10003730=f_t_1523867611653__r_t_1523867611653__v_t_1523867611653__r_c_0',
        'Host': 'www.zj-l-tax.gov.cn',
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    table = soup.find_all('table')[2]
    #print(table)
    div = table.find('div', id='czview1')
    #print(div)
    td1 = div.find('td', id='cyview1')  # 杭州市
    a1_list = td1.find_all('a')
    if len(a1_list) > 0:
        for tmp in a1_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '杭州市')

    td2 = div.find('td', id='cyview2')  # 温州市
    a2_list = td2.find_all('a')
    if len(a2_list) > 0:
        for tmp in a2_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '温州市')

    td3 = div.find('td', id='cyview3')  # 嘉兴市
    a3_list = td3.find_all('a')
    if len(a3_list) > 0:
        for tmp in a3_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '嘉兴市')

    td4 = div.find('td', id='cyview4')  # 湖州市
    a4_list = td4.find_all('a')
    if len(a4_list) > 0:
        for tmp in a4_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '湖州市')

    td5 = div.find('td', id='cyview5')  # 绍兴市
    a5_list = td5.find_all('a')
    if len(a5_list) > 0:
        for tmp in a5_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '绍兴市')

    td6 = div.find('td', id='cyview6')  # 金华市
    a6_list = td6.find_all('a')
    if len(a6_list) > 0:
        for tmp in a6_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '金华市')

    td7 = div.find('td', id='cyview7')  # 衢州市
    a7_list = td7.find_all('a')
    if len(a7_list) > 0:
        for tmp in a7_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '衢州市')

    td8 = div.find('td', id='cyview8')  # 舟山市
    a8_list = td8.find_all('a')
    if len(a8_list) > 0:
        for tmp in a8_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '舟山市')

    td9 = div.find('td', id='cyview9')  # 台州市
    a9_list = td9.find_all('a')
    if len(a9_list) > 0:
        for tmp in a9_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '台州市')

    td10 = div.find('td', id='cyview10')  # 丽水市
    a10_list = td10.find_all('a')
    if len(a10_list) > 0:
        for tmp in a10_list:
            clink = 'http://www.zj-l-tax.gov.cn' + tmp['href']
            download_detail(clink, '丽水市')

def download_detail(link, area):
    url = link
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'zh_choose=n; yfx_c_g_u_id_10003730=_ck18041616333116811896319053781; acw_tc=AQAAAAzMBlMorQYAvg3XOgSrbaW4FtIj; yfx_f_l_v_t_10003730=f_t_1523867611653__r_t_1523928532935__v_t_1523930796351__r_c_1; SERVERID=e146d554a29ee4143047c903abfbc3da|1523931505|1523930796',
        'Host': 'www.zj-l-tax.gov.cn',
        #Referer:http://www.zj-l-tax.gov.cn/col/col1229555/index.html
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tds = soup.find_all('td', class_='wzzw')
    # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人姓名、性别及身份证号码 财务负责人姓名、性别及身份证号码
    # 负有直接责任的中介机构信息 案件性质 主要违法事实 相关法律依据及税务处理处罚情况
    result = []
    for td in tds:
        tr = td.parent
        td = tr.find_all('td')[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('\"', '\\\"')
        result.append(td)
    result.append('浙江省')  # 所属省份
    result.append(area)  # 所属市
    result.append(link)  # 链接
    today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬取时间
    result.append(today)
    print(result)
    mysql_insert(result)

# 正文写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into zj_l_tax_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    download()