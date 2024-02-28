from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
import pandas as pd
import time 
import csv 

#브라우저 꺼짐 방지 효과 
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options) 

#코스트코 열기
driver.get("https://www.costco.co.kr/c/SpecialPriceOffers?itm_source=homepage&itm_medium=blueNav&itm_campaign=SpecialPriceOffers&itm_term=SpecialPriceOffers&itm_content=InternalCATSpecialPriceOffers&q=:price-desc:price:0%EC%9B%90%2B~%2B2%EB%A7%8C%EC%9B%90:price:2%EB%A7%8C%EC%9B%90%2B~%2B5%EB%A7%8C%EC%9B%90:price:5%EB%A7%8C%EC%9B%90%2B~%2B10%EB%A7%8C%EC%9B%90:price:10%EB%A7%8C%EC%9B%90%2B~%2B20%EB%A7%8C%EC%9B%90&sort=price-asc")

# 틈 두기
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/main/div[4]/sip-product-listing/div/div/div[2]/sip-page-slot/sip-product-list/div/section/div[3]/div/ul/sip-product-list-item[48]'))
)

# CSV 파일 열기
with open('costco_special_discount.csv', 'w', newline= '', encoding='utf-8') as file: 
    writer = csv.writer(file) 
    # CSV 파일의 헤더 작성 
    writer.writerow(['Title', 'Price', 'Img', 'Detail_txt', 'Detail_img'])

    for i in range(0,48): 
        element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[4]/sip-product-listing/div/div/div[2]/sip-page-slot/sip-product-list/div/section/div[3]/div/ul/sip-product-list-item[2]/li/div[2]/div[2]/div/a[1]'))
        )
        #요소 클릭
        driver.find_elements(By.CSS_SELECTOR,"a.lister-name.js-lister-name")[i].click()
        try: 
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="product_details"]/div/div/div/button'))
            )
        except: pass
        #배열에 추가
        img = driver.find_element(By.XPATH, "/html/body/main/div[4]/sip-product-details-page/sip-product-details/div/sip-product-image-panel/div/div/div[1]/div[1]/div/div/sip-image-zoom/div/sip-media[1]/picture/img").get_attribute("src")
        title = driver.find_element(By.CSS_SELECTOR,"h1.product-name").text
        price = driver.find_element(By.CSS_SELECTOR,"span.notranslate.ng-star-inserted").text
    
        #상세보기 버튼 클릭
        try: 
            driver.find_element(By.CSS_SELECTOR, "button.view-more__button.ng-star-inserted").click()
            time.sleep(2)
        except: 
            pass

        #배열에 추가
        file = driver.find_element(By.CSS_SELECTOR, "div.wrapper_itemDes")
        try:  
            detail_img = file.find_element(By.TAG_NAME, "img").get_attribute("src")
        except: 
            pass
        try: 
            detail_txt = file.text
        except: 
            detail_txt = ' '
        
        #줄 추가
        writer.writerow([title, price, img, detail_txt, detail_img])

        #뒤로 가기
        driver.back()


'''
#product 상품명 뽑기
product_list = driver.find_elements(By.CSS_SELECTOR, "a.lister-name.js-lister-name")
title = []
for i in product_list: 
    title.append(i.text) 

#product 가격 뽑기
product_price = driver.find_elements(By.CSS_SELECTOR, "span.notranslate.ng-star-inserted")
price_list = [] 
for i in product_price: 
    price_list.append(i.text)
price = price_list[0:len(product_list)]

#product img src 뽑기 
product_image = driver.find_elements(By.CSS_SELECTOR, "img.ng-star-inserted")
img = [] 
for i in product_image : 
    if "jpg" in i.get_attribute("src"):
        img.append(i.get_attribute("src"))
img = img[0:len(title)]

#상세페이지 img src 뽑기


#데이터 프레임 생성
df = pd.DataFrame({'상품 제목': title, '가격': price, '이미지URL': img})
df.to_excel('c:/Users/김민성/Desktop/코스트코/products.xlsx', index=False)
'''