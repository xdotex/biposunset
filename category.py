#카테고리 파트(이미 써져 있는 액셀에서 파일에 추가하기)

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv


# 네이버 쇼핑 열기
url = 'https://search.shopping.naver.com/search'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)


# 기존 CSV 파일 읽기
with open('costco_event_all_test1.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    headers = next(reader)  # 헤더 읽기
    headers.append('카테고리 코드')  # 새로운 열 이름 추가

#카테고리 코드 파일 열기
with open('category.csv', 'r') as category_file : 

#행으로 work 시작
rows = []
    for row in reader:
    #제품명 검색 
    #네이버 쇼핑에서 카테고리 get(리스트로 관리)
    #카테고리 액셀 파일에서 검색 후 카테고리 코드 찾기
        row.append(category_code)  # 각 행에 새로운 데이터 추가
        rows.append(row)

# 새로운 CSV 파일에 쓰기
with open('costco_event_all.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(headers)  # 헤더 쓰기
    writer.writerows(rows)  # 행 데이터 쓰기