import pymysql
import requests
import time
from bs4 import BeautifulSoup

def download():
    url = 'http://tax.hainan.gov.cn/topic/62.jspx'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=XlrWS1GIk6kJXqywy4LxKZmTMICBlfwZtg1vnNsWQhbkBr38SOVd!122300920; sto-id-2080-pool_himhwzn_j3=DHGEGIAKCJCA; yfx_c_g_u_id_10003737=_ck18041809224113560751647711513; yfx_f_l_v_t_10003737=f_t_1524014561333__r_t_1524014561333__v_t_1524014561333__r_c_0; yfx_mr_f_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; gwdshare_firstime=1524014568388; yfx_mr_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003737=; sdmenu_my_menu1=0100000; sdmenu_my_menu2=001; sdmenu_my_menu0=001000000000000000000',
        'Host': 'tax.hainan.gov.cn',
        #Referer:http://tax.hainan.gov.cn/
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    my_menu0 = soup.find('div', id='my_menu0')
    divs = my_menu0.find_all('div')
    for div in divs[1:]:
        area_name = div.find('span').get_text()
        value = div.find('input')['value']
        download_by_area(value, area_name)

def download_by_area(value, area_name):
    url = 'http://tax.hainan.gov.cn/zdaj/zdajlmmx.jspx?zdajfl=0&data={}&zdajtype='.format(value)
    headers = {
        'Accept': 'application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=XlrWS1GIk6kJXqywy4LxKZmTMICBlfwZtg1vnNsWQhbkBr38SOVd!122300920; sto-id-2080-pool_himhwzn_j3=DHGEGIAKCJCA; yfx_c_g_u_id_10003737=_ck18041809224113560751647711513; yfx_f_l_v_t_10003737=f_t_1524014561333__r_t_1524014561333__v_t_1524014561333__r_c_0; yfx_mr_f_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; gwdshare_firstime=1524014568388; yfx_mr_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003737=; sdmenu_my_menu1=0100000; sdmenu_my_menu2=001; sdmenu_my_menu0=001000000000000000000',
        'Host': 'tax.hainan.gov.cn',
        #Referer:http://tax.hainan.gov.cn/topic/62.jspx
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    items = soup.find_all('item')
    if len(items) != 0:
        for tmp in items:
            #print(tmp)
            clink = 'http://tax.hainan.gov.cn/zdaj/zdajdetail.jspx?wspzxh=' + tmp.find('wspzxh').get_text()
            download_detail(clink, area_name)

def download_detail(clink, area_name):
    url = clink
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=XlrWS1GIk6kJXqywy4LxKZmTMICBlfwZtg1vnNsWQhbkBr38SOVd!122300920; sto-id-2080-pool_himhwzn_j3=DHGEGIAKCJCA; yfx_c_g_u_id_10003737=_ck18041809224113560751647711513; yfx_mr_f_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; gwdshare_firstime=1524014568388; yfx_mr_10003737=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003737=; yfx_f_l_v_t_10003737=f_t_1524014561333__r_t_1524014561333__v_t_1524017237696__r_c_0; sdmenu_my_menu0=100000000000000000000; sdmenu_my_menu1=1000000; sdmenu_my_menu2=001',
        'Host': 'tax.hainan.gov.cn',
        #Referer:http://tax.hainan.gov.cn/zdaj/zdajdetail.jspx?wspzxh=20160505000000081587
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    trs = soup.find('table', class_='query_table').find_all('tr')
    result = []
    # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人或者负责人姓名、性别、证件名称及号码
    # 负有直接责任的财务负责人姓名、性别、证件名称及号码 负责直接责任的中介机构信息及其从业人员信息 案件性质
    # 主要违法违章事实和相关法律依据及税务处理处罚情况
    for tr in trs:
        td = tr.find_all('td')[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('\"', '\\\"').replace('\u3000', '')
        result.append(td)
    result.append('海南省')  # 所属省份
    result.append(area_name)  # 所属市
    result.append(clink)  # 链接
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
    sql = 'insert into hn_l_tax_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    download()