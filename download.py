#!/usr/bin/env python3
import requests
from sql import DBSession, Avatar
import os
from functools import partial
from asyncio import get_event_loop, wait, sleep

my_proxies = {"http": "socks5://127.0.0.1:1086", "https": "socks5://127.0.0.1:1086"}


headers = {

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    # "Host": "steamcdn-a.akamaihd.net",
    # "If-Modified-Since": "Tue, 09 Feb 2016 01:08:05 GMT",
    # "If-None-Match": "56b93c11-ec2",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
}

# 56b93bf5-1f3d
# 56b93c07-1b48

async def get_html(url, headers, proxies, timeout):
    loop = get_event_loop()
    html = await loop.run_in_executor(None, partial(requests.get, url=url, headers=headers, proxies=proxies, timeout=timeout))
    return html

async def save_file(fname, html):
    with open(fname, 'wb+') as f:
        f.write(html.content)

session = DBSession()


async def update_db(url):
    session.merge(url)
    session.commit()

async def delete_db(url):
    session.delete(url)
    session.commit()

async def down(urlObj):
    url = urlObj.url
    fname = "avatars" + "/" + urlObj.game_id + "_" + url[url.rfind('/')+1:]

    if os.path.exists(fname):
#        print('file exist.')
        urlObj.scraped = True
        await update_db(urlObj)
        return

    print("Scrping\t{}...".format(urlObj.id))
    html = await get_html(url, headers, my_proxies, 10)

    if (html.status_code == 404):
        print("404 Not found... ")
        await delete_db(urlObj)
        return

    if len(html.content) and len(html.text)  == 0:
        print("Failed {}".format(urlObj.url))
        headers["If-None-Match"] = html.headers.get("Etag")
        html = await get_html(url, headers, my_proxies, 10)
        if len(html.content) != 0:
            print("Success retry...")
        else:
            print("Fail retry...")
            return

    print("Save\t{}".format(urlObj.id))
    await save_file(fname, html)

    urlObj.scraped = True
    await update_db(urlObj)

def reset():
    avs = session.query(Avatar).all()
    for a in avs:
        a.scraped=False
    session.commit()

if __name__ == '__main__':
    # reset()
    if not os.path.exists('./avatars'):
    	os.mkdir('./avatars')

    old_remain = session.query(Avatar).filter_by(scraped=False).count()
    all = session.query(Avatar).count()

    tasks = []
    urlObjs =  session.query(Avatar).filter_by(scraped=False).all()
    tasks.extend([down(urlObj) for urlObj in urlObjs])
    print("Loop begin...")
    loop = get_event_loop()
    loop.run_until_complete(wait(tasks))
    loop.close()
    remain = session.query(Avatar).filter_by(scraped=False).count()
    print("\n\n\n====================\nOld Complete:\t{:.3f} %\n\tComplete:\t{:.3f} % \n=================\n".format((1 - old_remain * 1.0/all)*100,(1 - remain * 1.0/all)*100))

