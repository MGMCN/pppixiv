import requests

res = requests.post("http://127.0.0.1:5000/getIllustListByUid", data={"uid": "4837211"})
print('call getIllustListByUid api', res.text)

res = requests.post("http://127.0.0.1:5000/getIllustRanking", data={"mode": "day"})
print('call getIllustRanking api', res.text)

res = requests.get("http://127.0.0.1:5000/getTrendingTags")
print('call getTrendingTags api', res.text)
