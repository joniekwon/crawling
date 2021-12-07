from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
from urllib import request as rq

# [CODE 01] 네이버 증권 뉴스 크롤링.
def crollingStockNews(start_page, end_page):
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
    browser = webdriver.Chrome('./WebDriver/chromedriver.exe')
    browser.get(url)

    stockBtn = browser.find_element(By.CLASS_NAME, 'snb_s25')
    stockBtn.click()

    dataCover = []
    titles = []     # 기사 제목
    abstracts = []  # 기사 요약
    urls = []       # 기사 URL
    publishers= []  # 언론사
    for page in range(start_page-1,end_page+1):
        if page >1:
            url= f"https://news.naver.com/main/list.naver?mode=LS2D&sid2=258&sid1=101&mid=shm&date=20211028&page={page}"
            browser.get(url)
            print(f"url: {url}")
        else:
            print(f"url: {url}")
        title = browser.find_elements(By.CSS_SELECTOR,"#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a")
        #article_url = browser.find_elements(By.CSS_SELECTOR,"#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a")
        abstract = browser.find_elements(By.CSS_SELECTOR,"#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.lede")
        publisher = browser.find_elements(By.CSS_SELECTOR,
                                         "#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing")
        for i in range(len(title)):
            n_title = title[i].text
            n_article_url = title[i].get_attribute('href')
            urls.append(n_article_url)
            n_abstract = abstract[i].text
            n_publisher = publisher[i].text
            titles.append(n_title.replace("'", '"'))
            abstracts.append(n_abstract.replace("'", '"'))
            publishers.append(n_publisher.replace("'", '"'))
            print(f"title: {n_title}")
            print(f"article_url: {n_article_url}")
            print(f"abstract: {n_abstract}")

    imgs = []       # 기사 이미지
    writers = []    # 기자명
    for idx, i in enumerate(urls):
        browser.get(i)

        try:
            writer = browser.find_element(By.CSS_SELECTOR,"#articleBody > div.byline > p").text
            writer = writer.replace("'", '"').split()[0]    # 기자명 뒤에 따옴표 있을경우 통일하고 뒷내용 제거
            writer = writer.split('(')[0]       # 기자명 뒤에 괄호 있을 경우 제거하고 기자명만 저장
            writers.append(writer)
        except Exception as e1:
            writers.append('')

        try:
            newsImg = browser.find_element(By.CSS_SELECTOR, "#articleBodyContents > span > img")
            n_newsImg = newsImg.get_attribute('src')
            rq.urlretrieve(n_newsImg, './newsThum/thum_' + str(idx) + '.jpg')

            imgs.append('thum_'+str(idx)+'.jpg')
        except Exception as e2:
            imgs.append('')

    dataCover.append(titles)
    dataCover.append(publishers)
    dataCover.append(writers)
    dataCover.append(abstracts)
    dataCover.append(urls)
    dataCover.append(imgs)
    return dataCover

# [CODE 02] MariaDB에 크롤링한 데이터 업데이트
def updateNewsDB(data):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           port=3306,
                           password='0000',
                           db='stocknewsdb',
                           charset='utf8'
                          )
    cur = conn.cursor()

    t, p, w, a, u, th = data[0], data[1], data[2], data[3], data[4], data[5]
    for i in range(len(data[0])):
        n_title = t[i]
        n_publisher = p[i]
        n_writer = w[i]
        n_abstract = a[i]
        n_news_url = u[i]
        n_img_name = th[i]

        sql = 'INSERT INTO tbl_stocknews_v2(' \
              'n_title, n_publisher, n_writer, n_abstract,  n_news_url, n_img_name,n_reg_date) ' \
              'VALUES(%s, %s, %s, %s, %s, %s, NOW());'
        cur.execute(sql, (n_title, n_publisher, n_writer, n_abstract, n_news_url, n_img_name))
        conn.commit()

    conn.close()


if __name__ == "__main__":
    start = int(input("탐색할 시작 페이지:"))
    end = int(input("탐색할 종료 페이지:"))
    stockNews = crollingStockNews(start,end)            # [CODE 01] 네이버 증권 뉴스 크롤링
    #updateNewsDB(stockNews)       # [CODE 02] MariaDB에 크롤링한 데이터 업데이트

