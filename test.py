import requests

# res = requests.post("http://127.0.0.1:3333/getIllustListByUid", data={"uid": "4837211"})
res = requests.get("http://127.0.0.1:3333/getIllustListByUid")

print(res.text)
