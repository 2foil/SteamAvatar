#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import execjs
import time
from functools import partial
from sql import Avatar, Game, DBSession
from asyncio import get_event_loop,wait,sleep
import datetime

session = DBSession()
my_proxies = {"http": "socks5://127.0.0.1:1086", "https": "socks5://127.0.0.1:1086"}

url = "https://steamcommunity.com/actions/GameAvatars/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0", "Connection": "keep-alive",
    "Cookie": "sessionid=c5045b2e92e1843eaee4d49b; steamCountry=US%7C0c073361a74f5f85df3fb56d14323c7c; timezoneOffset=28800,0; _ga=GA1.2.1371899900.1528283841; _gid=GA1.2.685553443.1528283841",
    "Host": "steamcommunity.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
}

timeout = 10

async def get_html():
    loop = get_event_loop()
    html = await loop.run_in_executor(None, partial(requests.get, url=url, headers=headers, proxies=my_proxies, timeout=10))
    return html


async def scrap():
    time = datetime.datetime.now().strftime("%M:%S:%f")
    print("Scrap : {} ...".format(time))
    html = await get_html()
    print("Parse : {} ...".format(time))
    await parse(html.text)
    print(" Done : {} ...".format(time))


async def get_jsObj(response):
    bsObj = BeautifulSoup(response, 'lxml')
    mainBody = bsObj.find('div', id="mainBodySingle")
    scripts = bsObj.find_all('script', type="text/javascript")
    script = scripts[-1]
    jsObj = execjs.eval(script.text[0:-1])

    return jsObj, mainBody

async def parse_game(ggg, v):
    for i in range(len(v)):
        url = v[i][:-11] + '_full' + v[i][-4:]
        avatar = Avatar(url=url, game_id=ggg.id, scraped=False)
        session.add(avatar)
    session.commit()

async def add_game(game, k):
    if session.query(Game).filter_by(name=game[:-1].strip()).first():
        return None
    ggg = Game(name=game[:-1].strip(), id=k, )
    session.add(ggg)
    session.commit()
    return ggg

async def parse(response):
    print("\t Parsing: get_jsObj ...")
    jsObj, mainBody = await get_jsObj(response)


    for k,v in jsObj.items():
        ddd = mainBody.find('div', id="image_group_scroll_"+k)
        game = ddd.next_sibling.next_sibling.next_sibling.text
        ggg = await add_game(game, k)
        if(ggg == None):
            # print("\tExist...")
            continue

        await parse_game(ggg, v)

if __name__ == '__main__':
    old_num = session.query(Avatar).count()
    loop = get_event_loop()
    tasks = [scrap() for i in range(100)]
    loop.run_until_complete(wait(tasks))
    loop.close()
    new_num = session.query(Avatar).count()

    print("\n\n\n=======================\n\tOld: {}\tNew: {}\n\tDelta: {:.4f} %\n=======================\n".format(old_num, new_num, (new_num-old_num)*100/old_num))

