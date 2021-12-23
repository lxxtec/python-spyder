import requests
from bs4 import BeautifulSoup
import pandas as pd
pages=list(range(0,250,25))

def request_douban(url):
    htmls=[]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def get_htmls():
    htmls=[]
    for idx in pages:
        htmls.append(request_douban(f"https://movie.douban.com/top250?start={idx}&filter="))
    return htmls


def save_results():
    results = {
        '排名': [],
        '名称': [],
        '主演': [],
    }
    htmls=get_htmls()
    for html in htmls:
        soup=BeautifulSoup(html,'html.parser')
        for tag in soup.find_all(attrs={'class':'item'}):
            rank=tag.find('em').string
            name=tag.find('span',class_='title').string
            author=tag.p.get_text()

            results['排名'].append(rank)
            results['名称'].append(name)
            results['主演'].append(author)
            print(rank,' | ',name,' | ',author)
    df=pd.DataFrame(results)
    df.to_excel('save.xlsx',sheet_name='temper',index=False)


if __name__=='__main__':
    save_results()
