
import requests
from sql import Game, DBSession
import os

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


def down():
    session = DBSession()

    games = session.query(Game).all()

    for game in games:

        urls = game.avatars

        for i in range(len(urls)):
            url = urls[i].url

            if urls[i].scraped:
                continue

            fname = "avatars" + "/" + game.id + "_" + str(i+1) + "." +url.split('.')[-1]

            if os.path.exists(fname):
                urls[i].scraped = True
                session.merge(urls[i])

            html = requests.get(url, headers=headers, proxies=my_proxies, timeout = 10)

            if len(html.content) == 0:
                continue

            with open(fname, 'wb+') as f:
                f.write(html.content)
            print("Save "+game.id + ": "+str(i+1))

            urls[i].scraped = True
            session.merge(urls[i])

        session.commit()