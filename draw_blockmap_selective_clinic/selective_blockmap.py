#선별 진료소 수와 시도별 인구수 정보를 조합하여 블록맵 그리기

import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', None)      #27행 할당할때 에러출력 하지 않기

clinic_GeoData = pd.read_csv('./data/선별진료소_concat.csv',index_col=0, encoding='CP949', engine='python')
addr = pd.DataFrame(clinic_GeoData['address'].apply(lambda v:v.split()[:2]).tolist(),columns=('시도','군구'))

#print(addr['시도'].unique())
#print(addr['군구'].unique())

#print(addr[addr['군구']=='보듬7로20']) #412
addr.iloc[412] = ['세종특별자치시','세종시']          #군구에 바로 도로명주소가 시작됨 ㅠㅠ

#print(addr['군구'].unique())


addr['시도군구']=addr.apply(lambda r:r['시도']+' '+r['군구'], axis=1)
addr['count']=0         #count열 생성
addr_group = pd.DataFrame(addr.groupby(['시도','군구','시도군구'],as_index=False).count())
addr_group = addr_group.set_index('시도군구')       #'시도군구' 컬럼을 데이터프레임 병합에 사용할 인덱스로 설정
print(f"addr_group: \n{addr_group}")

population = pd.read_excel('./data/행정구역_시군구_별__성별_인구수_2.xlsx')
population = population.rename(columns = {'행정구역(시군구)별(1)':'시도','행정구역(시군구)별(2)':'군구'})
# print(f"population: \n{population}")


for element in range(0, len(population)):
    population['군구'][element] = population['군구'][element].strip()

population['시도군구']= population.apply(lambda r: r['시도'] + ' ' + r['군구'], axis=1)
population = population[population.군구 != '소계']      #소계행은 필요없으므로 삭제
# print(f"population: \n{population}")

population = population.set_index("시도군구")   # 병합의 기준이 될 인덱스를 '시도군구'로 설정
print(f"population: \n{population}")

addr_population_merge = pd.merge(addr_group,population,  how='inner',  left_index=True, right_index=True)
print(f"addr_population_merge: \n{addr_population_merge}")

local_MC_Population = addr_population_merge[['시도_x', '군구_x',  'count', '총인구수 (명)']]
local_MC_Population = local_MC_Population.rename(columns = {'시도_x': '시도', '군구_x': '군구','총인구수 (명)': '인구수' })

MC_count = local_MC_Population['count']
local_MC_Population['MC_ratio'] = MC_count.div(local_MC_Population['인구수'], axis=0)*100000
print(f"local_MC_Population.head():\n{local_MC_Population.head()}")

#시각화

from matplotlib import pyplot as plt
from matplotlib import rcParams, style
style.use('ggplot')

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

MC_count = local_MC_Population[['count']]
MC_count = MC_count.sort_values('count', ascending = False)
plt.rcParams["figure.figsize"] = (25,5)
MC_count.plot(kind='bar', rot=90)
#plt.show()
plt.savefig('.\\data\\' + 'MC_count.png')

MC_ratio = local_MC_Population[['MC_ratio']]
MC_ratio = MC_ratio.sort_values('MC_ratio', ascending = False)
plt.rcParams["figure.figsize"] = (25,5)
MC_ratio.plot(kind='bar', rot=90)
#plt.show()
plt.savefig('.\\data\\' + 'MC_ratio.png')
import os
path = os.getcwd()
data_draw_korea = pd.read_csv(path+'\\data\\data_draw_korea.csv', index_col=0, encoding='UTF-8', engine='python')
print(f"data_draw_korea.head():\n{data_draw_korea.head()}")
data_draw_korea['시도군구']= data_draw_korea.apply(lambda r: r['광역시도'] + ' ' + r['행정구역'], axis=1)
data_draw_korea = data_draw_korea.set_index("시도군구")
print(f"data_draw_korea.head():\n{data_draw_korea.head()}")
data_draw_korea_MC_Population_all = pd.merge(data_draw_korea,local_MC_Population,  how='outer',  left_index=True, right_index=True)
print(f"data_draw_korea_MC_Population_all.head():\n{data_draw_korea_MC_Population_all.head()}")


BORDER_LINES = [[(3, 2), (5, 2), (5, 3), (9, 3), (9, 1)], # 인천
                [(2, 5), (3, 5), (3, 4), (8, 4), (8, 7), (7, 7), (7, 9), (4, 9), (4, 7), (1, 7)], # 서울
                [(1, 6), (1, 9), (3, 9), (3, 10), (8, 10), (8, 9),(9, 9), (9, 8), (10, 8), (10, 5), (9, 5), (9, 3)], # 경기도
                [(9, 12), (9, 10), (8, 10)], # 강원도
                [(10, 5), (11, 5), (11, 4), (12, 4), (12, 5), (13, 5),(13, 4), (14, 4), (14, 2)], # 충청남도
                [(11, 5), (12, 5), (12, 6), (15, 6), (15, 7), (13, 7),(13, 8), (11, 8), (11, 9), (10, 9), (10, 8)], # 충청북도
                [(14, 4), (15, 4), (15, 6)], # 대전시
                [(14, 7), (14, 9), (13, 9), (13, 11), (13, 13)], # 경상북도
                [(14, 8), (16, 8), (16, 10), (15, 10),(15, 11), (14, 11), (14, 12), (13, 12)], # 대구시
                [(15, 11), (16, 11), (16, 13)], # 울산시
                [(17, 1), (17, 3), (18, 3), (18, 6), (15, 6)], # 전라북도
                [(19, 2), (19, 4), (21, 4), (21, 3), (22, 3), (22, 2), (19, 2)], # 광주시
                [(18, 5), (20, 5), (20, 6)], # 전라남도
                [(16, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10)], # 부산시
                ]

def draw_blockMap(blockedMap, targetData, title, color):
    # 흰색 라벨 임계값 정의.
    whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + min(blockedMap[targetData])
    datalabel = targetData
    vmin = min(blockedMap[targetData])
    vmax = max(blockedMap[targetData])

    #blockedMap.to_csv('./blockmap.csv', encoding='cp949')#블록맵 데이터 확인해보기..
    blockedMap = blockedMap.dropna() #결측치 제거. 결측치 존재할 경우 pivot에서 에러 발생
    #print(blockedMap.isna().sum())
    mapdata = blockedMap.pivot(index='y', columns='x', values=targetData)
    #print(f"mapdata:{mapdata}")

    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
    #print(f"masked_mapdata:{masked_mapdata}")

    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=color, edgecolor='#aaaaaa', linewidth=0.5)

    # 지역 이름 표시
    for idx, row in blockedMap.iterrows():
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

        # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다. (중구, 서구)
        if row['광역시도'].endswith('시') and not row['광역시도'].startswith('세종'):
            dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
            if len(row['행정구역']) <= 2:
                dispname += row['행정구역'][-1]
        else:
            dispname = row['행정구역'][:-1]

        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 9.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                     fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)

    # 시도 경계 그린다.
    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=4)

    plt.gca().invert_yaxis()
    # plt.gca().set_aspect(1)
    plt.axis('off')

    cb = plt.colorbar(shrink=.2, aspect=10)
    cb.set_label(datalabel)

    plt.tight_layout()

    plt.savefig('.\\data\\' + 'blockMap_' + targetData + '.png')

    plt.show()


draw_blockMap(data_draw_korea_MC_Population_all, 'count', '행정구역별 선별진료소 수', 'Blues')
draw_blockMap(data_draw_korea_MC_Population_all, 'MC_ratio', '행정구역별 인구수 대비 선별진료소 비율', 'Reds')