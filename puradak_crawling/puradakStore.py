from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select #select 태그 선택할때사용.

def puradak_store(result):
    puradak_URL = "https://www.puradakchicken.com/startup/store.asp"
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')
    wd.get(puradak_URL)
    time.sleep(1)  # 웹페이지 연결할 동안 1초 대기
    wd.find_element(By.CSS_SELECTOR, "#areaidx > option:nth-child(1)").click()

    for page in range(1,35):
        if page > 1:
            #nextBtn = wd.find_element(By.CSS_SELECTOR, "li:nth-child(%d) > div > a.btn.next" %i)
            nextBtn = wd.find_element(By.CLASS_NAME, "next")        # 다음 버튼
            wd.execute_script('arguments[0].click()', nextBtn)      # 다음 버튼 클릭

        for i in range(2, 22): #1페이지당 20개의 매장이 노출됨.
            try:
                time.sleep(1)  # 스크립트 실행 할 동안 1초 대기
                html = wd.page_source
                soupPRD = BeautifulSoup(html, 'html.parser')
                store_name_h2 = soupPRD.select(f"#result_search > li:nth-of-type({i}) > span > p.name")
                store_name = store_name_h2[0].string
                print(store_name)  # 매장 이름 출력
                store_doro = soupPRD.select(f"#result_search > li:nth-of-type({i}) > span > p.juso > span.doro")[0].string #도로명 주소
                store_phone = soupPRD.select(f"#result_search > li:nth-of-type({i}) > span > p.tel")[0].string #전화번호
                store_phone = store_phone.split()[2]           #연락처: 는 제외하고 전화번호만 가져오기
                print(store_phone)
                print(store_doro)
                result.append([store_name] + [store_doro] + [store_phone])

            except:
                continue
    return

def main():
    result = []
    print('PURADAK store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    puradak_store(result)  

    PRD_tbl = pd.DataFrame(result, columns=('store', 'address', 'phone'))
    PRD_tbl.to_csv('./data/puradak_store.csv', encoding='cp949', mode='w', index=True)


if __name__ == '__main__':
    main()
