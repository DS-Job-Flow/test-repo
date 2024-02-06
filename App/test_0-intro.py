import os
import time
import pandas as pd
import streamlit as st
from stqdm import stqdm
from glob import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument('--disable-popup-blocking')


## page setting
st.set_page_config(
    page_title='Intro'
)
st.title('Intro')
st.write('')


## 스트림릿 사용 방법 링크 제공
st.markdown('### Streamlit 사용 방법')
st.write('이 페이지를 활용하는 방법에 대해 알아보려면 [해당 링크](https://balanced-park-5a8.notion.site/c2f2b1a1677a464b8d80e225d296f803#0a35451ece3a4dc9b9fbf4bdfd92b7b7)를 참조하세요.')
st.write('')
st.write('')


## OpenAI API Key 발급 방법 링크 제공
st.markdown('### OpenAI API Key 발급 방법')
st.write('OpenAI API Key 발급 방법에 대해 알아보려면 [해당 링크](https://quartz-beluga-805.notion.site/API-Oragnization-ID-cd8f03ffd7864dd6bfc4d1dc7b80b0b9?pvs=4)를 참조하세요.')
st.write('')
st.write('')



###########################################################################################



## 스크롤 끝까지
def scroll(driver):
    scroll_location = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        scroll_height = driver.execute_script('return document.body.scrollHeight')
        if scroll_location == scroll_height:
            break
        else:
            scroll_location = driver.execute_script('return document.body.scrollHeight')
    driver.implicitly_wait(3)


## 스크롤 한 번만
def scroll_one(driver):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    driver.implicitly_wait(3)


## 수집명, 수집 개수, 첫번째 값 반환
def elem_return_0(Name, List):
    return print(f'\n{Name} *** {len(List)}\n{List[0]}')


## 수집명, 수집 개수 반환
def elem_return_1(Name, List):
    return print(f'\n{Name} *** {len(List)}')



###########################################################################################



## 원티드 수집
def Wanted(KEYWORD):

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                              options=options,)
    driver.get(f'https://www.wanted.co.kr/search?query={KEYWORD}&tab=position')
    driver.implicitly_wait(2)
    scroll(driver)

    # 검색 키워드 출력
    print(f'\n\n##### {KEYWORD} #####')

    # 데이터 수집
    Lin = [] # 링크
    Tit = [] # 타이틀
    Com = [] # 회사
    Loc = [] # 위치

    # 공고 개수
    num = driver.find_element(By.XPATH, '//*[@id="search_tabpanel_position"]/div/div[1]/h2').text
    num = int(num.replace('포지션', ''))
    for i in stqdm(range(1, num+1), desc='링크, 타이틀, 회사, 위치'):
        try:
            # 링크
            p_0 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a').get_attribute('href')
            Lin.append(p_0)                       

            # 타이틀
            p_1 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/strong').text
            Tit.append(p_1)

            # 회사
            p_2 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/span[1]/span[1]').text
            Com.append(p_2)                       

            # 위치
            p_3 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/span[1]/span[2]').text
            Loc.append(p_3)                    
        except Exception as e:
            st.write(e)
            break

    # 데이터 출력
    elem_return_0('링크', Lin)
    elem_return_0('타이틀', Tit)
    elem_return_0('회사', Com)
    elem_return_0('위치', Loc)

    # 데이터 수집
    Ctn_0 = [] # 주요업무
    Ctn_1 = [] # 자격요건
    Ctn_2 = [] # 우대사항

    for i in stqdm(range(num), desc='주요업무, 자격요건, 우대사항'):
        driver.get(Lin[i])
        scroll_one(driver)
        time.sleep(1)
        execute = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button/span[2]')
        driver.execute_script("arguments[0].click();", execute)
        time.sleep(1)

        try:
            # 주요업무
            p_4 = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[1]').text
            Ctn_0.append(p_4)

            # 자격요건
            p_5 = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[2]').text
            Ctn_1.append(p_5)

            # 우대사항
            p_6 = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[3]').text
            Ctn_2.append(p_6)

        except Exception as e:
            st.write(e)
            break

    driver.close()

    # 데이터 출력
    elem_return_1('주요업무', Ctn_0)
    elem_return_1('자격요건', Ctn_1)
    elem_return_1('우대사항', Ctn_2)

    # 데이터프레임 생성
    df = pd.DataFrame({
        'Title' : Tit,
        'Company' : Com,
        'Content_0' : Ctn_0, 
        'Content_1' : Ctn_1, 
        'Content_2' : Ctn_2,   
        'Link' : Lin,
        'Location' : Loc,
        'label' : f'{KEYWORD}',
        'platform': 'wanted',         
    })
    keyword_csv_file = f'{path}/{KEYWORD}.csv'
    df.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')

    return Tit, Com, Ctn_0, Ctn_1, Ctn_2, Lin, Loc



###########################################################################################



## st.button()    
# 빈 폴더 및 파일 생성
now = datetime.now()
now_name = now.strftime('%Y%m%d')
path = '../src'
if not os.path.exists(path):
    os.makedirs(path)

# 버튼 클릭
KEYWORDS = ['데이터 분석가', '데이터 사이언티스트']
st.markdown('### 데이터 수집')
if st.button('크롤링 실행'):
    if not os.path.exists(f'{path}/{now_name}_wanted.csv'):
        files_del = glob(f'{path}/*.csv')
        for file_del in files_del:
            os.remove(file_del)
        # 원티드 크롤링 시작 
        for KEYWORD in KEYWORDS:
            st_info = st.info(f'원티드 "{KEYWORD}" 크롤링 진행 중')
            Wanted(KEYWORD)

            time.sleep(1)
            st_info.empty()
            st_success = st.success(f'원티드 "{KEYWORD}" 크롤링 진행 완료')
            time.sleep(1)
            st_success.empty()

        # File Merge
        st_info = st.info('원티드 데이터 처리 중')
        DA = pd.read_csv(f'{path}/{KEYWORDS[0]}.csv')
        DS = pd.read_csv(f'{path}/{KEYWORDS[1]}.csv')
        df = pd.concat([DA, DS], axis=0)
        df.to_csv(f'{path}/{now_name}_wanted.csv', index=False, encoding='utf-8-sig')
        df = pd.read_csv(f'{path}/{now_name}_wanted.csv')

        # 원티드 Location 전처리 
        for i in range(0, len(df)):
            s_0 = df.Location[i].split(' · ')
            df.Location[i] = s_0[0]
        df.to_csv(f'{path}/{now_name}_wanted.csv', index=False, encoding='utf-8-sig')

        time.sleep(1)
        st_info.empty()
        st_success = st.success('원티드 데이터 처리 완료')
        time.sleep(1) 
        st_success.empty()

        # File Remove
        os.remove(f'{path}/{KEYWORDS[0]}.csv')
        os.remove(f'{path}/{KEYWORDS[1]}.csv')
    else:
        st_info = st.info('생성된 파일이 있습니다.')
        time.sleep(1)
        st_info.empty()