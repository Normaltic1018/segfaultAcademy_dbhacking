# step 1 웹 요청하고 응답 받기.
import urllib.request
import urllib.parse
import re

# 본인 실습 시스템의 URL 경로를 입력하세요!
url = ""

data = {'UserId': 'mario','Password':'mariosuper','Submit':'Login'}
data = urllib.parse.urlencode(data).encode()

cookie = 'PHPSESSID=nn91fov2c3j46bbaa9mb88qdft;'
req = urllib.request.Request(url, data=data)

req.add_header('cookie',cookie)

response = urllib.request.urlopen(req)
res_text = response.read().decode()

print(res_text)
