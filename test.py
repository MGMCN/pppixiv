import requests

res = requests.post("http://127.0.0.1:3333/getIllustListByUid", data={"uid": "4837211"})
print('call getIllustListByUid api', res.text)

res = requests.post("http://127.0.0.1:3333/getIllustRanking", data={"mode": "day"})
print('call getIllustRanking api', res.text)

res = requests.get("http://127.0.0.1:3333/getTrendingTags")
print('call getTrendingTags api', res.text)

res = requests.post("http://127.0.0.1:3333/getIllustUrl", data={"illust_id": "59580629"})
print('call getIllustUrl api', res.text)
