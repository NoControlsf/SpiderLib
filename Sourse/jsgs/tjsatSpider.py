import requests
from bs4 import BeautifulSoup

def download(cid, cname):
    url = 'http://wzcx.tjsat.gov.cn/cx_cxqyxx.action'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #Content-Length:33
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'yfx_c_g_u_id_10003175=_ck18041613233810998321115570367; yfx_f_l_v_t_10003175=f_t_1523856218073__r_t_1523856218073__v_t_1523856218073__r_c_0; _gscs_949898263=23856219f0xx1z51|pv:1; _gscbrs_949898263=1; JSESSIONID=ED133EE55D5C899FD836AB346CB67B92; _gscu_949898263=2385621940vyck51',
        'Host': 'wzcx.tjsat.gov.cn',
        #Origin:http://wzcx.tjsat.gov.cn
        #Referer:http://wzcx.tjsat.gov.cn/cx_zdwfaj.action?szsf=11200000000
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    form_data = {
        'szsf': 11200000000,
        'fjdm': cid
    }
    wb_data = requests.post(url, headers=headers, data=form_data)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup)


def parse():
    pass


def tjsatSpider():
    url = 'http://wzcx.tjsat.gov.cn/cx_zdwfaj.action?szsf=11200000000'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'yfx_c_g_u_id_10003175=_ck18041613233810998321115570367; yfx_f_l_v_t_10003175=f_t_1523856218073__r_t_1523856218073__v_t_1523856218073__r_c_0; _gscs_949898263=23856219f0xx1z51|pv:1; _gscbrs_949898263=1; JSESSIONID=ED133EE55D5C899FD836AB346CB67B92; _gscu_949898263=2385621940vyck51',
        'Host': 'wzcx.tjsat.gov.cn',
        #Referer:http://www.tjsat.gov.cn/
        #Upgrade-Insecure-Requests:1
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
    }
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tg_table = soup.find_all('table')[3]
    #print(tg_table)
    trs = tg_table.find_all('tr')
    for tr in trs[4:]:
        cid = tr.find('td')['id']
        cname = tr.find('td').get_text()
        print(cid)
        print(cname)
        download(cid, cname)


if __name__ == "__main__":
    tjsatSpider()