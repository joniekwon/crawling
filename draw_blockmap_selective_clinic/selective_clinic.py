#selective_clinic == triage room
#선별진료소 위치 지도에 마커 찍는 코드
#
import pandas as pd
import folium
import glob

def name_conv(addr):            #지역 이름 통일을 위해
    addr_new = []
    for i in range(len(addr)):
        if addr[i][0] == "서울":
            addr[i][0] = "서울특별시"
        elif addr[i][0] == "서울시":
            addr[i][0] = "서울특별시"
        elif addr[i][0] == "부산시":
            addr[i][0] = "부산광역시"
        elif addr[i][0] == "부산":
            addr[i][0] = "부산광역시"
        elif addr[i][0] == "인천":
            addr[i][0] = "인천광역시"
        elif addr[i][0] == "광주":
            addr[i][0] = "광주광역시"
        elif addr[i][0] == "대전시":
            addr[i][0] = "대전광역시"
        elif addr[i][0] == "대전":
            addr[i][0] = "대전광역시"
        elif addr[i][0] == "대구":
            addr[i][0] = "대구광역시"
        elif addr[i][0] == "울산시":
            addr[i][0] = "울산광역시"
        elif addr[i][0] == "울산":
            addr[i][0] = "울산광역시"
        elif addr[i][0] == "세종시":
            addr[i][0] = "세종특별자치시"
        elif addr[i][0] == "경기":
            addr[i][0] = "경기도"
        elif addr[i][0] == "충북":
            addr[i][0] = "충청북도"
        elif addr[i][0] == "충남":
            addr[i][0] = "충청남도"
        elif addr[i][0] == "전북":
            addr[i][0] = "전라북도"
        elif addr[i][0] == "전남":
            addr[i][0] = "전라남도"
        elif addr[i][0] == "경북":
            addr[i][0] = "경상북도"
        elif addr[i][0] == "경남":
            addr[i][0] = "경상남도"
        elif addr[i][0] == "제주":
            addr[i][0] = "제주특별자치도"
        elif addr[i][0] == "제주도":
            addr[i][0] = "제주특별자치도"
        elif addr[i][0] == "제주시":
            addr[i][0] = "제주특별자치도"
        elif addr[i][0] == "강원":
            addr[i][0] = "강원도"

        addr_new.append(' '.join(addr[i]))
    return addr_new

# 행정구역 이름 정리(표준화)

"""
#pandas Warning 출력 모드
mode.chained_assignment', 'warn': (SettingWithCopyWarning이 출력되는) 디폴트 입니다.
mode.chained_assignment', 'raise': SettingWithCopyException 오류를 발생시킵니다.
mode.chained_assignment', None : 해당 경고 자체를 하지 않습니다.
"""
def purifyAddress(file_name):
    data = pd.read_csv(f'./data/{file_name}.csv', encoding='CP949', index_col=0, header=0, engine='python')
    addr = []
    for address in data.주소:
        addr.append(str(address).split())
    #print(f"addr:{addr}")
    #addr_unique = pd.DataFrame(addr)[0].unique()
    #print(f"addr_unique:{addr_unique}")

    addr_new = name_conv(addr)      #동일한 지역명 통일시켜줌
    #print(f"addr_new:{addr_new}")
    clinics = []
    for clinic in data.진료소명:
        clinics.append(str(clinic).strip())
    print(f"clinics:{clinics}")

    df_addr = pd.DataFrame({'name':clinics,'address':addr_new}) # 진료소명과 정제된 주소지를 데이터프레임에 넣음
    print(f"df_addr.head():{df_addr.head()}")
    df_addr.to_csv(f'./data/{file_name}_purify.csv', encoding='CP949')            #csv로 내보내기

# 함수로 변경 --> divCSV_upto100rows(file_name)
# df_addr1 = pd.DataFrame({'name':clinics[:101],'address':addr_new[:101]})
# df_addr2 = pd.DataFrame({'name':clinics[101:201],'address':addr_new[101:201]})
# df_addr3 = pd.DataFrame({'name':clinics[201:301],'address':addr_new[201:301]})
# df_addr4 = pd.DataFrame({'name':clinics[301:401],'address':addr_new[301:401]})
# df_addr5 = pd.DataFrame({'name':clinics[401:501],'address':addr_new[301:401]})
# df_addr6 = pd.DataFrame({'name':clinics[501:601],'address':addr_new[501:601]})
# df_addr7 = pd.DataFrame({'name':clinics[601:],'address':addr_new[601:]})
#
# df_addr1.to_csv('./clinic_address1.csv', encoding='CP949')
# df_addr2.to_csv('./clinic_address2.csv', encoding='CP949')
# df_addr3.to_csv('./clinic_address3.csv', encoding='CP949')
# df_addr4.to_csv('./clinic_address4.csv', encoding='CP949')
# df_addr5.to_csv('./clinic_address5.csv', encoding='CP949')
# df_addr6.to_csv('./clinic_address6.csv', encoding='CP949')
# df_addr7.to_csv('./clinic_address7.csv', encoding='CP949')


def divCSV_uptoNrows(file_name, N=100):             # 100개 이상 좌표 변환 시간이 오래걸리므로 100개씩 나누어 작업하기 위해 N은 하나의 csv파일에 들어갈 행의 수
    data = pd.read_csv(f'./data/{file_name}_purify.csv', encoding='CP949', index_col=0, header=0, engine='python')
    clinics = data.name
    ad = data.address
    cell_idx = 0
    iter = len(data) // N
    for i in range(iter+1):
        next_idx = cell_idx + N
        # if i==(iter-1):       #마지막 파일 남는 데이터 처리하려고 추가했는데 추가안해도 에러가 안나서 생략
        #     df_addr = pd.DataFrame({'name': clinics[cell_idx:], 'address': addr_new[cell_idx:]})
        #     df_addr.to_csv(f'./temp/{file_name}_div{i+1}.csv', encoding='CP949')
        # else:
        df_addr = pd.DataFrame({'name': clinics[cell_idx:next_idx], 'address': ad[cell_idx:next_idx]})
        df_addr.to_csv(f'./data/{file_name}_div{i+1}.csv', encoding='CP949')
        cell_idx = next_idx
    return

def concat_CSV_all(file_name):               #좌표 변환한 csv파일을 다시 한 개의 파일로 합치기 위해 만듦.
    all_files = glob.glob(f"./data/convSHP/{file_name}_div*.shp.csv")          #file_name_div로 시작하는 csv파일명을 모두 불러옴
    #print(all_files)

    all_files_data = []
    for file in all_files:              # 각각의 파일을 데이터 프레임으로 불러옴
        data_frame = pd.read_csv(file, encoding='CP949', index_col=0, header=0, engine='python')
        all_files_data.append(data_frame)
    #print(all_files_data)
    all_files_data_concat = pd.concat(all_files_data, axis=0, ignore_index=True)

    all_files_data_concat.to_csv(f'./data/{file_name}_concat.csv', encoding='CP949')



if __name__=="__main__":
    file_name = '선별진료소'
    #purifyAddress(file_name)
    #divCSV_uptoNrows(file_name)
    #좌표 변환한 csv파일 : 선별진료소_div1.shp.csv
    #concat_CSV_all(file_name)

    map_osm = folium.Map(location=[37.559978,126.975291], zoom_start=15)
    map_osm.save("./map.html")

    clinic_GeoData = pd.read_csv(f'./data/{file_name}_concat.csv', encoding='CP949', engine='python')
    map_clinic = folium.Map(location=[37.559978, 126.975291], zoom_start=15)

    for i, clinic in clinic_GeoData.iterrows():
        folium.Marker(location=[clinic['위도'], clinic['경도']], popup=clinic['name'],
                      icon=folium.Icon(color='red', icon='star')).add_to(map_clinic)
    map_clinic.save(f'./data/{file_name}_map.html')
