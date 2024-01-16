import os
import time
import pandas as pd
import streamlit as st
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen, HTTPError
import re

path = './Data'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='오늘의 채용공고'
)
st.title('오늘의 채용공고')
st.write('')


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


## 원티드 수집
def Wanted(KEYWORD):

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
    for i in range(1, num+1):
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
    Ctn = [] # 공고내용

    for i in Lin:
        driver.get(i)
        driver.implicitly_wait(2)
        scroll_one(driver)

        # 공고내용
        try:
            p_4 = driver.find_element(By.CLASS_NAME, 'JobDescription_JobDescription__VWfcb').text
            Ctn.append(p_4)
        except Exception as e:
            st.write(e)
            break

    driver.close()

    # 데이터 출력
    elem_return_1('공고내용', Ctn)

    # 데이터프레임 생성
    df = pd.DataFrame({
        'Title' : Tit,
        'Company' : Com,
        'Content' : Ctn,   
        'Link' : Lin,
        'Location' : Loc,
        'label' : f'{KEYWORD}'         
    })
    keyword_csv_file = f'{path}/{KEYWORD}.csv'
    df.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')
    df = pd.read_csv(keyword_csv_file)

    return Tit, Com, Ctn, Lin, Loc


## 채용공고 아웃풋
def posting_output(df, posting):
    IDX = df.loc[df.label == f'{posting}'].index.tolist()
    st.write(f'#### {posting}')
    st.write('파란색 글씨를 누르면 해당 채용공고로 이동됩니다.')
    for i in IDX:
        st.write(f'{i}. {com_list[i]}, [{tit_list[i]}]({lin_list[i]})')


## st.button()
KEYWORDS = ['데이터 분석가', '데이터 사이언티스트']

# 빈 파일 생성
now_csv_file = f'{path}/{now_name}.csv'

# 버튼 클릭
if st.button('크롤링 실행'):
    if not os.path.exists(now_csv_file):
        # 크롤링 시작 
        st_info = st.info('크롤링 진행 중')
        for KEYWORD in KEYWORDS:
            Tit, Com, Ctn, Lin, Loc = Wanted(KEYWORD)

        time.sleep(1)
        st_info.empty()
        st_success = st.success('크롤링 완료')
        time.sleep(1)
        st_success.empty()

        # Data Preprocessing
        # merge
        st_info = st.info('데이터 처리 중')

        DA = pd.read_csv(f'{path}/{KEYWORDS[0]}.csv')
        DS = pd.read_csv(f'{path}/{KEYWORDS[1]}.csv')
        df = pd.concat([DA, DS], axis=0)
        df.to_csv(now_csv_file, index=False, encoding='utf-8-sig')
        df = pd.read_csv(now_csv_file)

        # Location
        for i in range(0, len(df)):
            s_0 = df.Location[i].split(' · ')
            df.Location[i] = s_0[0]
        df.to_csv(now_csv_file, index=False, encoding='utf-8-sig')

        time.sleep(1)
        st_info.empty()
        st_success = st.success('데이터 처리 완료')
        time.sleep(1) 
        st_success.empty()

        # file remove
        os.remove(f'{path}/{KEYWORDS[0]}.csv')
        os.remove(f'{path}/{KEYWORDS[1]}.csv')
    else:
        st_info = st.info('생성된 파일이 있습니다.')
        time.sleep(1)
        st_info.empty()
st.write('')
st.write('')

# st.selectbox()
posting = st.selectbox(
    '직무',
    ('데이터 분석가', '데이터 사이언티스트'),
    index=None,
    placeholder='직무를 선택해 주세요.'
)
st.write('')
try:
    df = pd.read_csv(now_csv_file)
    com_list = df.Company.tolist()
    tit_list = df.Title.tolist()
    lin_list = df.Link.tolist()

    if posting == '데이터 분석가':
        posting_output(df, posting)
    if posting == '데이터 사이언티스트':
        posting_output(df, posting)
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. 크롤링 실행 버튼을 눌러주세요.')