import pandas as pd

from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By

import matplotlib.pyplot as plt


def lotto_WinNumbers(number):
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')
    lotto_URL = f"https://dhlottery.co.kr/gameResult.do?method=byWin"
    wd.get(lotto_URL)
    No = []
    numbers = [[],[],[],[],[],[]]
    bonus = []
    for i in range(number):
        selectNum = Select(wd.find_element(By.ID, 'dwrNoList'))
        selectNum.select_by_index(i)
        #wd.execute_script("void(0)")
        searchBtn = wd.find_element(By.CSS_SELECTOR,"#searchBtn")
        wd.execute_script('arguments[0].click()', searchBtn)

        no = wd.find_element(By.CSS_SELECTOR,"#article > div:nth-child(2) > div > div.win_result > h4 > strong").text#[:-1] #회차
        No.append(no)
        lotto6Nums = wd.find_elements(By.CSS_SELECTOR, "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span")#6개 번호
        lottoBonus = wd.find_element(By.CSS_SELECTOR,           #보너스 번호
                                     "#article > div:nth-child(2) > div > div.win_result > div > div.num.bonus > p > span").text
        "#article > div:nth-child(2) > div > div.win_result > div > div.num.bonus > p > span"
        print(f"{no} 당첨결과:", end=' ')

        for i, Number in enumerate(lotto6Nums):
            num = int(Number.text)
            numbers[i].append(num)
            print(num, end=' ')
        print(f'+ {lottoBonus}')
        bonus.append(int(lottoBonus))

    return No, numbers, bonus

# 크롤링한 데이터 cvs로 저장
def saveResult(result):
    no, numbers, bonus = result
    Lotto_tbl = pd.DataFrame({'No': no, 'Num1':numbers[0], 'Num2':numbers[1], 'Num3':numbers[2], 'Num4':numbers[3],
                             'Num5':numbers[4], 'Num6':numbers[5], 'Bonus':bonus}, index=None)
    Lotto_tbl.to_csv(f'./data/Lotto_WIN_NUMBER({result[0][-1]}~{result[0][0]}).csv', encoding='cp949', mode='w', index=True)


# 분석을 위해 저장된 csv 파일 불러오기
def loadCSV():
    lottoCSV = pd.read_csv("./data/Lotto_WIN_NUMBER(888회~987회).csv")
    lottoResult = pd.DataFrame(lottoCSV)
    result=[]
    no = lottoResult['No'].values.tolist()
    num1 = lottoResult['Num1'].values.tolist()
    num2 = lottoResult['Num2'].values.tolist()
    num3 = lottoResult['Num3'].values.tolist()
    num4 = lottoResult['Num4'].values.tolist()
    num5 = lottoResult['Num5'].values.tolist()
    num6 = lottoResult['Num6'].values.tolist()
    bonus = lottoResult['Bonus'].values.tolist()
    numbers=[]
    result.append(no)
    numbers.append(num1)
    numbers.append(num2)
    numbers.append(num3)
    numbers.append(num4)
    numbers.append(num5)
    numbers.append(num6)
    result.append(numbers)
    result.append(bonus)
    return result

def modMax(result):

    no, numbers, bonus = result
    length = len(no)
    print(f"최근 {length}회 분 당첨 번호 빈도 분석")
    lottoNum = numbers[0] + numbers[1]+ numbers[2] + numbers[3] + numbers[4] + numbers[5] +bonus
   # print(lottoNum)
    numberDict = {}
    for num in lottoNum:
        if num not in numberDict:
            numberDict[num] = 1
        else:
            numberDict[num] +=1

    modDict = {}
    for num in numberDict.values():
        if num not in modDict.keys():
            modDict[num] = []
    try:
        for key in numberDict.keys():
            modDict[numberDict[key]].append(key)
    except:
        pass
    #print(modDict) # 당첨 횟수 별 숫자
    print(f"가장 많이 당첨된 숫자 (총 {max(modDict.keys())} 회 당첨):{modDict[max(modDict.keys())]}")
    print(f"가장 적게 당첨된 숫자 (총 {min(modDict.keys())} 회 당첨):{modDict[min(modDict.keys())]}")

    print(numberDict)
    return numberDict

# 숫자 별 당첨 횟수 시각화 (수정 필요)
def drawHist(resultDict):
    keys = sorted(resultDict.keys())
    values = resultDict.values()
    # keyString = list(map(str, keys))
    # valuesString = list(map(str, values))
    plt.bar(keys, values)
    plt.show()

if __name__ == "__main__":
    work = int(input("작업을 선택하세요: 1. 크롤링, 2. 데이터 분석"))
    if work ==1:
        number = int(input("최근 몇 회까지의 당첨 번호를 조회할까요?"))
        result = lotto_WinNumbers(number)

        doSave = input("결과를 저장할까요? [y]/n")

        if doSave==(""or"y"or"Y"or"ㅛ"):
            saveResult(result)
    else:
        result = loadCSV()      #저장된 csv파일 가져오기
        resDict = modMax(result)          #빈도수 구하기
        drawHist(resDict)           #그래프 그리기
