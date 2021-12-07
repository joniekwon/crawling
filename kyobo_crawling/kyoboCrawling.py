import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def kyobo_best(sector):
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')

    sectors = {'분야 종합': ['A', 'Aa', 'KOR', 10], '소설': ['B', 'Ab', 'KOR', 1], '에세이': ['C', 'Ab', 'KOR', 1],
               '국내소설': ['D', 'Ab', 'KOR', 1], '국외소설': ['E', 'Ab', 'KOR', 1], '시': ['F', 'Ab', 'KOR', 1],
               '어린이': ['G', 'Ab', 'KOR', 1], '가정생활': ['H', 'Ab', 'KOR', 1], '인문': ['I', 'Ab', 'KOR', 1],
               '정치사회': ['J', 'Ab', 'KOR', 1], '경제경영': ['K', 'Ab', 'KOR', 1], '건강': ['L', 'Ab', 'KOR', 1],
               '교양과학': ['M', 'Ab', 'KOR', 1], '외국어': ['N', 'Ab', 'KOR', 1], '예술': ['Q', 'Ab', 'KOR', 1],
               '취미／스포츠': ['R', 'Ab', 'KOR', 1], 'TOEIC／TOEFL': ['S', 'Ab', 'KOR', 1], '유아': ['T', 'Ab', 'KOR', 1],
               '종교': ['U', 'Ab', 'KOR', 1], '아동만화': ['V', 'Ab', 'KOR', 1], '요리／와인': ['a', 'Ab', 'KOR', 1],
               '역사／문화': ['b', 'Ab', 'KOR', 1],
               '자기계발': ['c', 'Ab', 'KOR', 1], '여행': ['d', 'Ab', 'KOR', 1], '기술／컴퓨터': ['e', 'Ab', 'KOR', 1],
               '만화': ['f', 'Ab', 'KOR', 1], '청소년': ['g', 'Ab', 'KOR', 1], '장르소설': ['08', 'Bk', 'EBK', 5],
               '서양도서': ['h', 'Ab', 'KOR', 1], '일본도서': ['i', 'Ab', 'KOR', 1]
               }
    kyobo_URL = f"http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb={sectors[sector][2]}&linkClass={sectors[sector][0]}&range=1&kind=0&orderClick=D{sectors[sector][1]}"  # 분야별
    wd.get(kyobo_URL)

    titles = []
    publishers = []
    authors = []
    pYears = []
    detail_URLs = []

    for page in range(1,sectors[sector][3]+1):              # 페이지 수만큼 반복
        if page>1:
            wd.execute_script(f"_go_targetPage('{page}')")          # 스크립트 실행해서 다음 페이지로 넘김
            time.sleep(1)
        bookNames = wd.find_elements(By.CSS_SELECTOR, "#main_contents > ul > li > div.detail > div.title > a")

        for book in range(len(bookNames)):
            detail_URLs.append(bookNames[book].get_attribute('href'))
            titles.append(bookNames[book].text)

        if sector=="장르소설" or sector=="서양도서" or sector=="일본도서":
            infos = wd.find_elements(By.CSS_SELECTOR,"#main_contents > ul > li > div.detail > div.author")
            for idx, info in enumerate(infos):
                author = info.text.split("|")[0].strip()
                author= author.replace(" 저자 더보기",'')
                publisher = info.text.split("|")[1]
                pYear = info.text.split("|")[2]
                authors.append(author)
                publishers.append(publisher)
                pYears.append(pYear)
                print(titles[idx], author, publisher, pYear, sep=' | ')
            break
        # 장르소설, 서양도서, 일본도서는 따로 만들거나 다르게 처리해야할듯. 임시방편
    if sector != ("장르소설" and "서양도서" and "일본도서"):
        for index, url in enumerate(detail_URLs):
            wd.get(url)
            time.sleep(1)
            try:
                author = wd.find_element(By.CLASS_NAME, "detail_author").text
                publisher = wd.find_element(By.CSS_SELECTOR,
                                            "#container > div:nth-child(4) > form > div.box_detail_point > div.author > span:nth-child(3) > a").text
                pYear = wd.find_element(By.CLASS_NAME,
                                        "date").text  # container > div:nth-child(4) > form > div.box_detail_point > div.author > span.date
                authors.append(author)
                publishers.append(publisher)
                pYears.append(pYear)
            except:
                info = wd.find_element(By.CLASS_NAME, "txt_info")
                print(info.text)
                author = info.text.split("|")[0]
                publisher = info.text.split("|")[1]
                pYear = info.text.split("|")[2]
                authors.append(author)
                publishers.append(publisher)
                pYears.append(pYear)

            print(titles[index], author, publisher, pYear, sep=' | ')

    return titles, authors, publishers, pYears

def kyobo_best_all():
    sectors = ['분야 종합', '소설', '에세이', '국내소설', '국외소설', '시', '어린이', '가정생활',
               '인문', '정치사회', '경제경영', '건강', '교양과학', '외국어', '예술', '취미／스포츠',
               'TOEIC／TOEFL', '유아', '종교', '아동만화', '요리／와인', '역사／문화', '자기계발',
               '여행', '기술／컴퓨터', '만화', '청소년', '장르소설', '서양도서', '일본도서']

    for sector in sectors:
        titles, authors, publishers, pYears = kyobo_best(sector)
        KYOBO_tbl = pd.DataFrame({'title':titles, 'author':authors, 'publisher':publishers, 'publish_year':pYears}, index=None)
        KYOBO_tbl.to_csv(f'./data/kyobo_best({sector}).csv', encoding='cp949', mode='w', index=True)

def kyobo_best_one(sector):
    titles, authors, publishers, pYears = kyobo_best(sector)
    KYOBO_tbl = pd.DataFrame({'title': titles, 'author': authors, 'publisher': publishers, 'publish_year': pYears},
                             index=None)
    KYOBO_tbl.to_csv(f'./data/kyobo_best({sector}).csv', encoding='cp949', mode='w', index=True)

if __name__ == '__main__':
    print('KYOBO BOOK STORE crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    #kyobo_best_all()
    kyobo_best_one('일본도서')
    print('KYOBO BOOK STORE crawling SUCCESS.')

