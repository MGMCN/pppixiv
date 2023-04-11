# pppixiv
[![build](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml?logo=github)](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml?logo=github)
[![image](https://img.shields.io/docker/pulls/godmountain/pppixiv?logo=docker&logoColor=white)](https://hub.docker.com/r/godmountain/pppixiv)
[![issue](https://img.shields.io/github/issues/MGMCN/pppixiv?logo=github)](https://github.com/MGMCN/pppixiv/issues?logo=github)
[![license](https://img.shields.io/github/license/MGMCN/pppixiv)](https://github.com/MGMCN/pppixiv/blob/main/LICENSE)
![last_commit](https://img.shields.io/github/last-commit/MGMCN/pppixiv?color=red&logo=github)
  
Get links to all illustrations by a particular artist on pixiv.
## Usage
### Build with Docker
```bash
# build locally
$ docker build . -t pixiv
# run on detach
$ docker run -d -p 3333:5000 -e username="your_pixiv_accout_name" -e password="your_pixiv_account_password" pixiv
# run in foreground
$ docker run -it -p 3333:5000 -e username="your_pixiv_accout_name" -e password="your_pixiv_account_password" pixiv
```
If you successfully run this image up, you can run the test.py file to see the output. The first time will be slower because you have to get the pixiv token.
```bash
$ python3 test.py # Make sure you have the requests library installed
```
### Use DockerHub Image
```bash
$ docker pull godmountain/pppixiv:latest
$ docker run -d -p 3333:5000 -e username="your_pixiv_accout_name" -e password="your_pixiv_account_password" godmountain/pppixiv:latest
```

## Api for accessing our pixiv services
Visit```http://ip:port/getIllustListByUid```and post data ```{"uid":"xxx"}```.You will get 👇🏻
> status : 0 stands for failure while 1 stands for success  
> message : error message  
> list : returned data
```json lines
{
  "status": 1,
  "message": "message",
  "list": [
    {"title": "title1", "url": "url1"},
    {},
    {},
  ]
}
```

Visit```http://ip:port/getIllustRanking```and post data ```{"mode":"xxx"}```. (We have mode: day, week, month, day_male, day_female, week_original, week_rookie, day_manga) You will get 👇🏻
```json lines
{
  "status": 1,
  "message": "message",
  "list": [
    {"title": "title1", "url": "url1"},
    {},
    {},
  ]
}
```

Visit```http://ip:port/getTrendingTags```.
You will get 👇🏻
```json lines
{
  "status": 1,
  "message": "message",
  "list": [
    {"tag": "JP version(Unicode)", "translated_tag": "EN version"},
    {},
    {},
  ]
}
```
## Contributing
Contributions must be available on a separately named branch based on the latest version of the main branch.
