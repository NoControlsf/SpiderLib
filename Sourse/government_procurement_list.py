import requests
from bs4 import BeautifulSoup

def download():
    for i in range(2, 3):
        url = 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=004&catgorynum2=007&xiaqu=&type=2'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            #'Content-Length': '6305',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'lzzbj=20111113; ASP.NET_SessionId=agbc0q4553j0voidzwge3i55; __CSRFCOOKIE=fdfd96fa-eb4f-4ff8-a553-1073c4c66ddd',
            'Host': 'www.gxlzzb.com',
            #'Origin': 'http://www.gxlzzb.com',
            'Referer': 'http://www.gxlzzb.com/gxlzzbw//showinfo/jyxxmore.aspx?catgorynum1=004&catgorynum2=007&xiaqu=&type=2',
            #'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2990.0 Safari/537.36'
        }
        form_data = {
            '__CSRFTOKEN': '/wEFJGZkZmQ5NmZhLWViNGYtNGZmOC1hNTUzLTEwNzNjNGM2NmRkZA==',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'D38D4441',
            '__EVENTTARGET': 'JyxxSearch1$Pager',
            '__EVENTARGUMENT': str(i),
            'JyxxSearch1$Pager_input': str(sp_fuc(i))
        }
        wb_data = requests.post(url, headers=headers, data=form_data)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        parse(soup)

def sp_fuc(i):
    if(i == 1):
        return 1
    else:
        return i-1


def parse(soup):
    print(soup)

if __name__ == "__main__":
    download()