import requests
from bs4 import BeautifulSoup
import execjs
import time
from sql import Avatar, Game, DBSession

def scrap():
    my_proxies = {"http": "socks5://127.0.0.1:1086", "https": "socks5://127.0.0.1:1086"}

    url = "https://steamcommunity.com/actions/GameAvatars/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0","Connection": "keep-alive",
        "Cookie": "sessionid=c5045b2e92e1843eaee4d49b; steamCountry=US%7C0c073361a74f5f85df3fb56d14323c7c; timezoneOffset=28800,0; _ga=GA1.2.1371899900.1528283841; _gid=GA1.2.685553443.1528283841",
        "Host": "steamcommunity.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
    }
    html = requests.get(url, headers=headers,proxies=my_proxies,timeout=5)

    parse(html.text)

def parse(response):
    session = DBSession()

    my_proxies = {"http": "socks5://127.0.0.1:1086", "https": "socks5://127.0.0.1:1086"}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "steamcdn-a.akamaihd.net",
        "If-Modified-Since": "Tue, 09 Feb 2016 19:15:37 GMT",
        "If-None-Match": "56ba3ad9-2f32",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
    }

    bsObj = BeautifulSoup(response,'lxml')
    mainBody = bsObj.find('div',id="mainBodySingle")

    scripts = bsObj.find_all('script', type="text/javascript")
    script = scripts[-1]
    jsObj = execjs.eval(script.text[0:-1])

    for k,v in jsObj.items():

        ddd = mainBody.find('div', id="image_group_scroll_"+k)
        game = ddd.next_sibling.next_sibling.next_sibling.text
        if session.query(Game).filter_by(name =game[:-1].strip()).first():
            print("Exist...")
            continue
        ggg = Game(name=game[:-1].strip(), id=k)
        session.add(ggg)
        session.commit()

        for i in range(len(v)):
            url = v[i][:-11]+'_full' + v[i][-4:]
            avatar = Avatar(url=url, game_id=ggg.id)
            session.add(avatar)

            print("Save "+ggg.name+" -> "+ str(i) +' ...')
        session.commit()

if __name__ == '__main__':
    for i in range(100):
        scrap()
    time.sleep(1)