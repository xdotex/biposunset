from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

url = 'https://www.costco.co.kr/events'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)

# 무한 스크롤
old_height = driver.execute_script("return document.body.scrollHeight") #스크롤을 위한 높이 가져옴
while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #페이지 끝으로 스크롤 다운
        try:
            WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.body.scrollHeight;") > old_height) #컨텐츠 로드 10초 대기
            old_height = driver.execute_script("return document.body.scrollHeight") #페이지 높이 업데이트
        except TimeoutException: #10초 조건 만족 안 하면 루프 종료
            break


# CSV 파일
with open('costco_event_all_test1.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # CSV 파일의 헤더 작성
    writer.writerow(['Title', 'Price', 'Sale_price', 'Real_price', 'Image URL'])

    # 제품들 링크
    products = driver.find_elements(By.CSS_SELECTOR, 'div.thumb a')

    # 제품별 정보 가져오기
    for product in products:
        # 새 탭에서 링크 열기
        link = product.get_attribute('href')
        driver.execute_script('window.open("{}");'.format(link))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        # 정보 추출
        try:
            title = driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text

            price = driver.find_element(By.CSS_SELECTOR, 'span.price-value span.notranslate.ng-star-inserted').text
            sale_price = driver.find_element(By.CSS_SELECTOR, 'span.discount-value span.notranslate.ng-star-inserted').text
            real_price = driver.find_element(By.CSS_SELECTOR, 'span.you-pay-value').text

            img = driver.find_element(By.CSS_SELECTOR, 'div.page-content.container.main-wrapper img.ng-star-inserted').get_attribute('src')

            # CSV 파일에 쓰기
            writer.writerow([title, price, sale_price, real_price, img])
        except Exception as e:
            print(e)
        
        # 현재 탭 닫기 및 원래 탭으로 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()