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
old_height = driver.execute_script("return document.body.scrollHeight") #스크롤을 위한 높이를 가져옵니다.
while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #페이지 끝으로 스크롤 다운
        try:
            WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.body.scrollHeight;") > old_height) #컨텐츠 로드 10초 대기
            old_height = driver.execute_script("return document.body.scrollHeight") #페이지 높이 업데이트
        except TimeoutException: #10초 조건 만족 안 하면 루프 종료
            break

# 상세 페이지 클릭
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[4]/sip-content-page/div/sip-page-slot[1]/sip-product-carousel[1]/sip-product-carousel-base/div/div/sip-carousel/owl-carousel-o/div/div[1]/owl-stage/div/div/div[1]/div/sip-product-carousel-item/div/span/div[1]/a'))
)
element.click()
time.sleep(3)

# CSV 파일 열기
with open('costco_event_test2.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # CSV 파일의 헤더 작성
    writer.writerow(['Title', 'Price', 'Sale_price', 'Real_price', 'Image URL'])

    # 리스트에서 타이틀, 이미지 url 가져오기
    try:
      title = driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text

      price = driver.find_element(By.CSS_SELECTOR, 'span.price-value span.notranslate.ng-star-inserted').text
      sale_price = driver.find_element(By.CSS_SELECTOR, 'span.discount-value span.notranslate.ng-star-inserted').text
      real_price = driver.find_element(By.CSS_SELECTOR, 'span.you-pay-value').text

      img = driver.find_element(By.CSS_SELECTOR, 'img.ng-star-inserted').get_attribute('src')

      # CSV 파일에 쓰기
      writer.writerow([title, price, sale_price, real_price, img])
    except Exception as e:
        print(e)

driver.quit()