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
    writer.writerow(['판매자 상품코드', '상품명', '코스트코판매가격', '실제표시가격','대표이미지', '추가이미지', '수입사', '원산지 직접입력', '상품정보제공고시 품명', '상품정보제공고시 모델명', '상품정보제공고시 인증허가사항'])

    # 제품들 링크
    products = driver.find_elements(By.CSS_SELECTOR, 'div.thumb a')

    # 제품별 정보 가져오기
    for product in products[:3]: # 3개만 가져오도록. 나중에 변경 필요.
        # 새 탭에서 링크 열기
        link = product.get_attribute('href')
        driver.execute_script('window.open("{}");'.format(link))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        # 정보 추출
        try:
            code = driver.find_element(By.CSS_SELECTOR, 'p.product-code span.notranslate').text
            sell_code = 'cc#'+code

            product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text
            price = driver.find_element(By.CSS_SELECTOR, 'span.notranslate.ng-star-inserted').text

            #최종판매가격(민성 추가)
            sell_price = int(round(1.95*float(price.replace('원','').replace(',','')) + 2175, -2))

            # 이미지
            images = driver.find_elements(By.CSS_SELECTOR, 'div.page-content.container.main-wrapper sip-product-details.ng-star-inserted div.primary-image-wrapper sip-media.zoomed-image.ng-star-inserted.is-initialized img.ng-star-inserted')
            main_img = images[0].get_attribute('src')
            img_urls = '\n'.join([img.get_attribute('src') for img in images[1:]])  # 이미지 URL을 개행문자로 연결

            # 상품정보제공고시 품명 = product_name
            # 상품정보제공고시 모델명 = product_name

            # 스펙 오픈 후 정보 업로드까지 기다리기
            elements = driver.find_element(By.CSS_SELECTOR, 'i.costco-icons.costco-icon-plus-sign').click()
            time.sleep(2)

            # 리스트로 관리(하위 html 정보에 접근할 수 있는 방법이 있는지? ex: tr 정보를 따온 후 거기의 td에 접근하는 법)
            attrib = driver.find_elements(By.CSS_SELECTOR, 'td.attrib')
            attrib_val = driver.find_elements(By.CSS_SELECTOR, 'td.attrib-val')
            spec = []
            for idx in range(0,len(attrib)): 
                spec.append([attrib[idx].text, attrib_val[idx].text])
            manufacture = None
            made_in = None
            KC = None
            for spec_list in spec:
                 if spec_list[0] == '제조자/수입자':
                      manufacture = spec_list[1]
                 if spec_list[0] == '제조국 또는 원산지':
                      made_in = spec_list[1]
                 if spec_list[0] == 'KC 인증 정보' :
                      KC = spec_list[1]

            # CSV 파일에 쓰기(sell price 추가)
            writer.writerow([sell_code, product_name, price, sell_price, main_img, img_urls, manufacture, made_in, product_name, product_name, KC])
        except Exception as e:
            print(e)
        
        # 현재 탭 닫기 및 원래 탭으로 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()