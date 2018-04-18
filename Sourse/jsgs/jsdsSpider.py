import re

import pymysql
import requests
from bs4 import BeautifulSoup

#下载链接
def download(areaname, areavalue):
    url = 'http://pub.jsds.gov.cn/jcms/jcms_files/jcms1/web1/site/module/jslib/bulletin/ajaxdata.jsp?startrecord=1&endrecord=4&perpage=15'
    headers = {
        'Accept': 'text/javascript, application/javascript, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        #Content-Length:56
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=DCCF4ECB0B47EBDFD773814E0080341E; yfx_c_g_u_id_10003729=_ck18041614323019663157559569389; yfx_f_l_v_t_10003729=f_t_1523860350933__r_t_1523860350933__v_t_1523860350933__r_c_0; hz6d_70722535_isuv=0; hz6d_70722535_guest_id=5ad446ce4b8cb0520c59fcc5; hz6d_70722535_member_id=setKfDefaultMemberId; hz6d_70722535_member_guest=%7B%22setKfDefaultMemberId%22%3A%225ad446ce4b8cb0520c59fcc5%22%7D; hz6d_identifyNum=e67a6502-877c-4029-8636-c6436f52fc6f',
        'Host': 'pub.jsds.gov.cn',
        #Origin:http://pub.jsds.gov.cn
        #Referer:http://pub.jsds.gov.cn/jcms/jcms_files/jcms1/web1/site/module/jslib/bulletin/bullenright.jsp?searhvalue=%E5%8D%97%E4%BA%AC-00823&searchkey=area
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    form_data = {
        'searhvalue': areavalue,
        'searchkey': 'area',
        'year': ''
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    recordset = re.findall(r'\[(.*?)\]', wb_data.text.replace('\n', '').replace('\r', '').replace('\t', ''))[0]
    trs = re.findall(r'<tr>(.*?)</tr>', recordset.replace('\n', '').replace('\r', '').replace('\t', ''))
    for tr in trs:
        trsoup = BeautifulSoup(tr, 'lxml')
        #print(trsoup)
        clink = trsoup.find('a')['href']
        print(clink)
        download_detail(clink, areaname)

#下载详情
def download_detail(clink, areaname):
    url = clink
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')
    table = soup.find('table').find('table')
    #print(table)
    trs = table.find_all('tr')
    result = []
    for tr in trs:
        # 纳税人名称 纳税人识别号 组织机构代码 注册地址 法定代表人姓名、性别及身份证号码 财务负责人姓名、性别及身份证号码
        # 负有直接责任的中介机构信息 案件性质 主要违法事实 相关法律依据及税务处理处罚情况 检查机关 公布机关
        td = tr.find_all('td')[1].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').replace('\"', '\\\"')
        result.append(td)
    result.append('江苏省')
    result.append(areaname)
    result.append(clink)
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
    sql = 'insert into jsds_detail values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()



if __name__ == "__main__":
    #download('南京', '南京-00823')
    #download('无锡', '无锡-00824')
    #download('常州', '常州-00826')
    #download('苏州', '苏州-00827')
    #download('连云港', '连云港-00829')
    download('泰州', '泰州-00834')