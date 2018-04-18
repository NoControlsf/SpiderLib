import pymysql
import requests
import time
from bs4 import BeautifulSoup

def download():
    url = 'http://dsj.hubei.gov.cn/xxgk/zdsswfaj/2017whs/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10003734=_ck18041711064812517378316773193; yfx_f_l_v_t_10003734=f_t_1523934408215__r_t_1523934408215__v_t_1523934408215__r_c_0',
        'Host': 'dsj.hubei.gov.cn',
        #Referer:http://dsj.hubei.gov.cn/xxgk/zdsswfaj/
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    ul = soup.find('ul', id='abc')
    tg_ul = soup.find('ul', class_='wzy_list_right_ul')
    #print(ul)
    #print(tg_ul)  # 武汉市 解析完地区链接后详细解析
    lis = tg_ul.find_all('li')
    if lis[0].find('a').get_text().replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '') != "暂无省级税收违法案件公布":
        for li in lis:
            clink = li.find('a')['href']
            title = li.find('a').get_text()
            bt_time = li.find('span').get_text()
            download_detail(clink, '武汉市', title, bt_time)

    a_list = ul.find_all('a')
    for a in a_list[1:]:
        area_link = 'http://dsj.hubei.gov.cn/xxgk/zdsswfaj' + a['href'].replace('.', '')
        area_name = a.get_text()
        #print(area_link)
        #print(area_name)
        search_by_area(area_link, area_name)

#检索其他市
def search_by_area(area_link, area_name):
    url = area_link
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10003734=_ck18041711064812517378316773193; yfx_f_l_v_t_10003734=f_t_1523934408215__r_t_1523934408215__v_t_1523934408215__r_c_0',
        'Host': 'dsj.hubei.gov.cn',
        #Referer:http://dsj.hubei.gov.cn/xxgk/zdsswfaj/
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tg_ul = soup.find('ul', class_='wzy_list_right_ul')
    lis = tg_ul.find_all('li')
    if lis[0].find('a').get_text().replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '') != "暂无省级税收违法案件公布":
        for li in lis:
            clink = li.find('a')['href']
            list = clink.split('/')
            title = li.find('a').get_text()
            bt_time = li.find('span').get_text()
            if list[0] != '.':
                download_detail(clink, area_name, title, bt_time)
            else:
                tg_link = area_link + list[-2] + '/' + list[-1]
                download_detail(tg_link, area_name, title, bt_time)

def download_detail(clink, area, title, bt_time):
    url = clink
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.hb-l-tax.gov.cn',
        #Referer:http://dsj.hubei.gov.cn/xxgk/zdsswfaj/2017whs/
        #Upgrade-Insecure-Requests:1
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    tables = soup.find_all('table', class_='MsoNormalTable')
    if len(tables) != 0:
        table = tables[-1]
        # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人或者负责人姓名、性别、证件名称及号码
        # 负有直接责任的财务负责人姓名、性别、证件名称及号码 负有直接责任的中介机构信息及其从业人员信息 案件性质
        # 主要违法事实和相关法律依据及税务处理处罚情况
        result = []
        trs = table.find_all('tr')
        if len(trs) == 9:
            for i in range(9):
                tr = trs[i]
                p = tr.find_all('td')[1].get_text().replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace('\xa0', '').replace('\u3000', '')
                result.append(p)
            result.append('湖北省')  # 所属省份
            result.append(area)  # 所属城市
            result.append(clink)  # 链接
            today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬取时间
            result.append(today)
            result.append(title)  # 标题
            result.append(bt_time)  # 发布时间
            print(result)
            mysql_insert(result)
        else:
            print('error')
    else:
        print('error')


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
    sql = 'insert into hb_l_tax_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    download()