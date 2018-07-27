

# SteamAvatar
![](https://img.shields.io/badge/python-3.5%2C%203.6%2C%203%2C7-blue.svg)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)

A crawler that scrap the Steam avatars.
# Usage
- Update urls and download.

```bash
$ git clone -b dev git@github.com:2foil/SteamAvatar.git
$ cd SteamAvatar
$ pip3 install -r requirements.txt 
$ python scrap.py
$ python download.py
```
- Only download the scraped urls in avatar.sqlite.

```bash
$ git clone git@github.com:2foil/SteamAvatar.git
$ cd SteamAvatar
$ pip3 install -r requirements.txt 
$ python download.py
```

# Result
![](./pics/avatars.png)
The avatars is saved at ```./avatars```
# Tech
- using python corotinue: async/await 
