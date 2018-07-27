# SteamAvatar
a crawler that scrap the Steam avatars.

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
