# pppixiv
[![build](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml?logo=github)](https://img.shields.io/github/actions/workflow/status/MGMCN/pppixiv/pr.yml?logo=github)
[![image](https://img.shields.io/docker/pulls/godmountain/pppixiv?logo=docker&logoColor=white)](https://hub.docker.com/r/godmountain/pppixiv)
[![issue](https://img.shields.io/github/issues/MGMCN/pppixiv?logo=github)](https://github.com/MGMCN/pppixiv/issues?logo=github)
[![license](https://img.shields.io/github/license/MGMCN/pppixiv)](https://github.com/MGMCN/pppixiv/blob/main/LICENSE)
![last_commit](https://img.shields.io/github/last-commit/MGMCN/pppixiv?color=red&logo=github)

A powerful Pixiv illustration download tool that supports batch one-click downloading of all illustrations by a specified artist.

## Usage
> For users in mainland China, please enable vpn service.
### Build with Docker
Build your docker image and run it.
```bash
# build locally
$ docker build . -t pixiv
# run on detach 
# -v will specify the folder where the illustrations will be downloaded
$ docker run -d -p 3333:5000 \
             -e username="your_pixiv_accout_name" \
             -e password="your_pixiv_account_password" \
             -v /Your/local/path/dir:/APP/Illusts pixiv
```
If you successfully run this image up, you can run the test.py file to see the output. The first time will be slower because you have to get the pixiv token.
```bash
$ python3 test.py # Make sure you have the requests library installed
```
### Use DockerHub Image
Pull our built image directly.
```bash
$ docker pull godmountain/pppixiv:latest
$ docker run -d -p 3333:5000 \
             -e username="your_pixiv_accout_name" \
             -e password="your_pixiv_account_password" \
             -v /Your/local/path/dir:/APP/Illusts godmountain/pppixiv:latest
```
### Run outside the docker container
Create .env file and Illusts folders.
```
.
├── .env 👈🏻 Paste your pixiv account and password into the .env file.
├── Illusts 👈🏻 Create the Illusts folder in the root directory of the project.
├── Dockerfile
├── LICENSE
├── README.md
├── app.py
├── image
├── main.py
├── requirements.txt
├── router
├── run.sh
├── services
├── static
├── templates
└── test.py
```
.env should like 👇🏻
```
username=xxx
password=xxx
port=xxx
```
Add chromedriver to your environment variable. (Notice : The chromedriver version should be the same as the chrome browser you downloaded.) Please google how to set chromedriver environment variables by yourself. 
Then execute the following two commands after you have set up chromedriver.
```bash
$ pip3 install -r requirements.txt
$ python3 main.py
```
### Solution for get token failure
If you encounter this problem below. 👇🏻 
```
DEBUG in main: =====================================================================================
DEBUG in main: Authorized on pixiv account your_account_name. Please wait for authentication.
DEBUG in pixiv: getToken error!
DEBUG in pixiv: getToken error!
DEBUG in pixiv: getToken error!
DEBUG in pixiv: getToken error!
DEBUG in pixiv: getToken error!
DEBUG in main: Failed to get token, please check if you are blocked by pixiv or possibly because of reCAPTCHA v2 detection.
DEBUG in main: Application ends gracefully.
DEBUG in main: =====================================================================================
```
You can try setting [headless](https://github.com/MGMCN/pppixiv/blob/dfda5cbbef2e966d664b22a5a20b5b6ac7bf9785/services/pixiv.py#L54) to False and then manually validate reCAPTCHA. Please note that when you use this approach, make sure you are running the pppixiv outside a docker container.
## Visit our dashboard
Visit```http://ip:port/dashboard```.You will see 👇🏻
Then enter the uid and click the search button, all the illustrations of the user with the specified uid will be searched and displayed on the right side.  

<img src="image/search.png" width = "85%" height = "85%"/>   
  
Click the download button and all illustrations will be downloaded. If the download is successful, the gray dot on the right will turn green. Failed downloads will turn red.  

<img src="image/download.png" width = "85%" height = "85%"/>   

After the illustration is downloaded successfully you will see the following message.

<img src="image/success.png" width = "85%" height = "85%"/>   

Click the Preview button to preview the illustration you just downloaded.

<img src="image/preview.png" width = "85%" height = "85%"/>  

The artist in this example is referenced from [仁井学](https://www.pixiv.net/users/17089321).
## Contributing
Contributions must be available on a separately named branch based on the latest version of the main branch.
