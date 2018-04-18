import pymysql
import requests
import time
from bs4 import BeautifulSoup

def download():
    url = 'http://www.gdltax.gov.cn/siteapps/webpage/gdltax/zdsswfaj/list1.jsp'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10000291=_ck18041715284919378454638942730; yfx_f_l_v_t_10000291=f_t_1523950129830__r_t_1523950129830__v_t_1523950129830__r_c_0; yfx_c_g_u_id_10000017=_ck18041715285216755397003728531; yfx_f_l_v_t_10000017=f_t_1523950132646__r_t_1523950132646__v_t_1523950132646__r_c_0; Hm_lvt_70bc8eb2313a4533e224ed24bd3ce148=1523950173; Hm_lpvt_70bc8eb2313a4533e224ed24bd3ce148=1523950173; yfx_c_g_u_id_10000023=_ck18041715293518675167903619235; yfx_f_l_v_t_10000023=f_t_1523950175836__r_t_1523950175836__v_t_1523950175836__r_c_0; yfx_c_g_u_id_10000018=_ck18041715293810731088076353894; yfx_f_l_v_t_10000018=f_t_1523950178046__r_t_1523950178046__v_t_1523950178046__r_c_0; Hm_lvt_5bd875b4619932123c7ee4eca943194a=1523950131; Hm_lpvt_5bd875b4619932123c7ee4eca943194a=1523950213; Hm_lvt_09b94e2fdcb4e670e1f24692ca5c0fcd=1523950234; Hm_lpvt_09b94e2fdcb4e670e1f24692ca5c0fcd=1523950234; yfx_c_g_u_id_10000021=_ck18041715303318975633495530539; yfx_f_l_v_t_10000021=f_t_1523950233873__r_t_1523950233873__v_t_1523950233873__r_c_0; JSESSIONID=W0LSgt9bDhHWauLzp3OPNQLU-mjf2FAxthlEhK1lIYaNiIU1mREg!942566452; _gscu_2017942901=23950177wuq6lv24; _gscs_2017942901=2395017701nq8y24|pv:3; _gscbrs_2017942901=1; Hm_lvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1523950178; Hm_lpvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1523950248',
        'Host': 'www.gdltax.gov.cn',
        #Referer:http://www.gdltax.gov.cn/gdsite/portal/gdsite/JUTPCVQ7NJJVBC65EB8L2LK3CAM3HJZX.htm
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    lis = soup.find('ul', id='navul').find('ul').find_all('li')
    for li in lis[1:]:
        area_link = 'http://www.gdltax.gov.cn/siteapps/webpage/gdltax/zdsswfaj/' + li.find('a')['href']
        area_name = li.find('a').get_text()
        download_by_area(area_link, area_name)

def download_by_area(area_link, area_name):
    url = area_link
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10000291=_ck18041715284919378454638942730; yfx_f_l_v_t_10000291=f_t_1523950129830__r_t_1523950129830__v_t_1523950129830__r_c_0; yfx_c_g_u_id_10000017=_ck18041715285216755397003728531; yfx_f_l_v_t_10000017=f_t_1523950132646__r_t_1523950132646__v_t_1523950132646__r_c_0; Hm_lvt_70bc8eb2313a4533e224ed24bd3ce148=1523950173; Hm_lpvt_70bc8eb2313a4533e224ed24bd3ce148=1523950173; yfx_c_g_u_id_10000023=_ck18041715293518675167903619235; yfx_f_l_v_t_10000023=f_t_1523950175836__r_t_1523950175836__v_t_1523950175836__r_c_0; yfx_c_g_u_id_10000018=_ck18041715293810731088076353894; yfx_f_l_v_t_10000018=f_t_1523950178046__r_t_1523950178046__v_t_1523950178046__r_c_0; Hm_lvt_5bd875b4619932123c7ee4eca943194a=1523950131; Hm_lpvt_5bd875b4619932123c7ee4eca943194a=1523950213; Hm_lvt_09b94e2fdcb4e670e1f24692ca5c0fcd=1523950234; Hm_lpvt_09b94e2fdcb4e670e1f24692ca5c0fcd=1523950234; yfx_c_g_u_id_10000021=_ck18041715303318975633495530539; yfx_f_l_v_t_10000021=f_t_1523950233873__r_t_1523950233873__v_t_1523950233873__r_c_0; JSESSIONID=W0LSgt9bDhHWauLzp3OPNQLU-mjf2FAxthlEhK1lIYaNiIU1mREg!942566452; _gscu_2017942901=23950177wuq6lv24; _gscs_2017942901=2395017701nq8y24|pv:3; _gscbrs_2017942901=1; Hm_lvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1523950178; Hm_lpvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1523950248',
        'Host': 'www.gdltax.gov.cn',
        #Referer:http://www.gdltax.gov.cn/gdsite/portal/gdsite/JUTPCVQ7NJJVBC65EB8L2LK3CAM3HJZX.htm
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    lis = soup.find('div', class_='select-list').find('ul').find_all('li')
    if len(lis) != 0:
        for li in lis:
            clink = 'http://www.gdltax.gov.cn/siteapps/webpage/gdltax/zdsswfaj/' + li.find('p', class_='title').find('a')['href']
            download_detail(clink, area_name)
        #font = soup.find('div', class_='page-num').find_all('font')[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        #ifont = int(font)
        #if ifont > 1:
         #   for i in range(2, ifont + 1):



def download_detail(clink, area_name):
    url = clink
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10000291=_ck18041715284919378454638942730; yfx_c_g_u_id_10000017=_ck18041715285216755397003728531; Hm_lvt_70bc8eb2313a4533e224ed24bd3ce148=1523950173; yfx_c_g_u_id_10000023=_ck18041715293518675167903619235; yfx_f_l_v_t_10000023=f_t_1523950175836__r_t_1523950175836__v_t_1523950175836__r_c_0; yfx_c_g_u_id_10000018=_ck18041715293810731088076353894; Hm_lvt_09b94e2fdcb4e670e1f24692ca5c0fcd=1523950234; yfx_c_g_u_id_10000021=_ck18041715303318975633495530539; yfx_f_l_v_t_10000021=f_t_1523950233873__r_t_1523950233873__v_t_1523950233873__r_c_0; yfx_f_l_v_t_10000291=f_t_1523950129830__r_t_1524011249780__v_t_1524011249780__r_c_1; Hm_lvt_5bd875b4619932123c7ee4eca943194a=1523950131,1524011254; Hm_lpvt_5bd875b4619932123c7ee4eca943194a=1524011254; yfx_f_l_v_t_10000017=f_t_1523950132646__r_t_1524011255886__v_t_1524011255886__r_c_1; yfx_f_l_v_t_10000018=f_t_1523950178046__r_t_1524011810797__v_t_1524011810797__r_c_1; _gscu_2017942901=23950177wuq6lv24; _gscs_2017942901=2401181044xpls21|pv:3; _gscbrs_2017942901=1; Hm_lvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1523950178,1524011811; Hm_lpvt_57bcaaa1ce098c7f5d3c32b9bb28d738=1524011822; JSESSIONID=Z17WLmo2Fm3IanJARTKDR-fThmde7KvxEYGOhQFHjbUaIl0O4bOo!-1231643075',
        'Host': 'www.gdltax.gov.cn',
        #Referer:http://www.gdltax.gov.cn/siteapps/webpage/gdltax/zdsswfaj/list1.jsp
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup)
    trs = soup.find('div', class_='info').find('table').find_all('tr')
    result = []
    # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人姓名、性别及身份证号码
    # 财务负责人姓名、性别及身份证号码 负有直接责任的中介机构信息 案件性质 发布时间 主要违法事实 相关法律依据及税务处理处罚情况
    for tr in trs:
        td = tr.find('td').get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('\"', '\\\"').replace('\u3000', '')
        result.append(td)
    result.append('广东省')  # 所属省份
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
    sql = 'insert into gd_l_tax_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    download()