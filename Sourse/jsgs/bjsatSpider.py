import re

import pymysql
import requests
from bs4 import BeautifulSoup

def download(pid, area, page):
    url = 'http://www.bjsat.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #Content-Length:186
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'route=cea6eaa088166cc5cc92f613997504aa; JSESSIONID=fsvL9d7oQUt6sIVktXBbsf696hru7KkUAozUwCFrTgjJSWKMUvB8!238112034!-1036950210; yfx_c_g_u_id_10003677=_ck18041608580110114246095548717; yfx_f_l_v_t_10003677=f_t_1523840280942__r_t_1523840280942__v_t_1523840280942__r_c_0; _va_id=2c731514832f3455.1523840282.1.1523841234.1523840282.; _va_ses=*',
        'Host': 'www.bjsat.gov.cn',
        #Origin:http://www.bjsat.gov.cn
        #Referer:http://www.bjsat.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    form_data = {
        'id': pid,
        'dq': area,
        'ajlx': 'null',
        'ndjd': 'null',
        'bz': 'dq',
        'dqy': page,
        'ymdx': '',
        'nsrmc': 'null',
        'nsrsbh': 'null',
        'zcdz': 'null',
        'zzjgdm': 'null',
        'fddbrmc': 'null',
        'fddbrsfzhm': 'null',
        'cwfzrmc': 'null',
        'cwfzrsfzhm': 'null',
        'orgCode': 11100000000
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    return soup

def download_by_id(pid, area, page):
    url = 'http://www.bjsat.gov.cn/bjsat/office/jsp/zdsswfaj/wwidquery'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #Content-Length:186
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'route=cea6eaa088166cc5cc92f613997504aa; JSESSIONID=fsvL9d7oQUt6sIVktXBbsf696hru7KkUAozUwCFrTgjJSWKMUvB8!238112034!-1036950210; yfx_c_g_u_id_10003677=_ck18041608580110114246095548717; yfx_f_l_v_t_10003677=f_t_1523840280942__r_t_1523840280942__v_t_1523840280942__r_c_0; _va_id=2c731514832f3455.1523840282.1.1523841234.1523840282.; _va_ses=*',
        'Host': 'www.bjsat.gov.cn',
        #Origin:http://www.bjsat.gov.cn
        #Referer:http://www.bjsat.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    form_data = {
        'id': pid,
        'dq': area,
        'ajlx': 'null',
        'ndjd': 'null',
        'bz': 'dq',
        'dqy': page,
        'ymdx': '',
        'nsrmc': 'null',
        'nsrsbh': 'null',
        'zcdz': 'null',
        'zzjgdm': 'null',
        'fddbrmc': 'null',
        'fddbrsfzhm': 'null',
        'cwfzrmc': 'null',
        'cwfzrsfzhm': 'null',
        'orgCode': 11100000000
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    return soup

def parse_link(soup, area):
    table = soup.find_all('table')[2]
    td = table.find('tr').find('td').get_text().replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '')
    if td != '没有找到相关数据':
        trs = table.find_all('tr')
        for tr in trs[:-1]:
            fuc_td = tr.find_all('td')[4]
            #print(fuc_td)
            record = re.findall(r"xx\(\'(.*?)\'\)", str(fuc_td).replace('\n', '').replace('\r', ''))[0]
            print(record)
            parse_detail(record, area, 1)

        last_tr = trs[len(trs)-1]
        #print(last_tr)
        page_msg = last_tr.find_all('td')[1].get_text()
        print(page_msg)
        page = re.findall(r"查询结果(.*?)页", str(page_msg).replace('\n', '').replace('\r', ''))[0]
        print(page)
        page_i = int(page)
        if page_i > 1:
            for i in range(2, page_i + 1):
                soup = download('', area, i)
                table = soup.find_all('table')[2]
                td = table.find('tr').find('td').get_text()
                if td != '没有找到相关数据':
                    trs = table.find_all('tr')
                    for tr in trs[:-1]:
                        fuc_td = tr.find_all('td')[4]
                        #print(fuc_td)
                        record = re.findall(r"xx\(\'(.*?)\'\)", str(fuc_td).replace('\n', '').replace('\r', ''))[0]
                        print(record)
                        parse_detail(record, area, i)


def parse_detail(record, area, page):
    soup = download_by_id(record, area, page)
    table = soup.find('table').find('table')
    #print(table)
    trs = table.find_all('tr')
    result = []
    for tr in trs[:-1]:
        # 纳税人名称 纳税人识别号或社会信用代码 组织机构代码 注册地址
        # 法定代表人或者负责人姓名、性别及身份证号码（或其他证件号码）
        # 违法期间法人代表或者负责人姓名、性别及身份证号码（或其他证件号码）
        # 负有直接责任的财务人员姓名、性别及身份证号码（或其他证件号码）
        # 负有直接责任的中介机构信息 案件性质 主要违法事实,相关法律依据及税务处理处罚情况
        td = tr.find_all('td')[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        result.append(td)
    result.append(record)  # id
    result.append('北京市')  # 直辖市
    result.append(area)  # 地区

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
    sql = 'insert into bjsat_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()




def bjsatSpider():
    areas = ['东城', '西城', '朝阳', '海淀', '丰台', '石景山', '门头沟', '房山', '通州', '顺义', '大兴', '昌平', '平谷', '怀柔', '密云', '延庆', '开发区', '西站', '燕山']
    for area in areas:
        soup = download('', area, 1)
        parse_link(soup, area)
    #soup = download('', '海淀', 1)
    #parse_link(soup, '海淀')

if __name__ == "__main__":
    bjsatSpider()