#카테고리 파트(이미 써져 있는 액셀에서 파일에 추가하기)
#costco_crawling이랑 이어지는 파일이 아닌 분리되는 코드로 작성(후속작업 진행)
from bs4 import BeautifulSoup 
import requests
import time
import csv 

# 기존 CSV 파일 읽기
with open('costco_event_all_test1.csv', 'r', encoding = 'utf-8') as input_file:
    reader = csv.reader(input_file)
    headers = next(reader)  # 헤더 읽기(csv 파일의 경우 이터레이터가 행)
    headers.append('카테고리 코드')  # 새로운 열 이름 추가
    #행으로 work 시작
    for row in reader:
    #제품명 검색 후 카테고리 get
        # 네이버 쇼핑 열기
        url = 'https://search.shopping.naver.com/search/all?query=' + row[1].replace(' ', '%20')
        response = requests.get(url)
        if response.status_code == 200: 
            html = response.text 
            soup = BeautifulSoup(html, 'html.parser')
            category_html = soup.select('#content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(5) > div > div > div.product_info_area__xxCTi > div.product_depth__I4SqY > span')
            category = [] 
            for content in category_html : 
                category.append(content.text)
            print(category)
        else : 
            print(response.status_code) 
        #카테고리 액셀 파일에서 검색 후 카테고리 코드 찾기
        with open('C:/Users/김민성/Desktop/코스트코/category.csv', 'r', encoding = 'utf-8') as category_file : 
            leader = csv.reader(category_file)
            for line in leader: 
                if line[1:] == category : 
                    category_code = line[0]
                    break
        if category_code is not None:  # 카테고리 코드가 찾아진 경우
            print(category_code)
        else:  # 카테고리 코드가 없는 경우
            print("카테고리 코드를 찾을 수 없습니다.")
# 다시 천천히 정리해보자.
        ''' row.append(category_code)  # 각 행에 새로운 데이터 추가
            rows.append(row)

        # 새로운 CSV 파일에 쓰기
        with open('costco_event_all.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(headers)  # 헤더 쓰기
            writer.writerows(rows)  # 행 데이터 쓰기'''