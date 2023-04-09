# pppixiv
[![build](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml)](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml)
[![issue](https://img.shields.io/github/issues/MGMCN/pppixiv)](https://github.com/MGMCN/pppixiv/issues)
[![license](https://img.shields.io/github/license/MGMCN/pppixiv)](https://github.com/MGMCN/pppixiv/blob/main/LICENSE)
![last_commit](https://img.shields.io/github/last-commit/MGMCN/pppixiv?color=red)
  
Get links to all illustrations by a particular artist on pixiv.
## Usage
```bash
docker build . -t pixiv # build locally
docker run -p 3333:5000 -e username="your_pixiv_accout_name" -e password="your_pixiv_account_password" pixiv
```
If you successfully run this image up, you can run the test.py file to see the output. The first time will be slower because you have to get the pixiv token.
```bash
python3 test.py # Make sure you have the requests library installed
```
