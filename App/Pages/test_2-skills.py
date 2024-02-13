import time
import openai
import pandas as pd
import streamlit as st
from datetime import datetime
from openai import OpenAI


path = '../src'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='네카라쿠배당토 채용공고 확인'
)
st.title('네카라쿠배당토 채용공고 확인')
st.write('')

## 데이터프레임 가져오기
try:
    df = pd.read_csv(f'{path}/{now_name}_wanted.csv')
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. Intro 페이지에서 크롤링 실행 버튼을 눌러주세요.')



###########################################################################################



## OpenAI Org-ID, API Key
ORGANIZATION_ID = 'your org-xxx'
OPENAI_API_KEY = 'your sk-xxx'

client = OpenAI(
    organization = ORGANIZATION_ID,
    api_key = OPENAI_API_KEY
)

## API Key 저장 및 확인
if st.button('OpenAI API Key 검증'):
    try:
        openai.api_key = OPENAI_API_KEY
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"}
            ],
        )
        st_success = st.success('API 키가 유효합니다.')
        time.sleep(1)
        st_success.empty()
    except Exception as e:
        st.error(f'API Key 검증 실패: {e}')
st.markdown('---')
st.write('')



###########################################################################################



# 코드 이 밑으로 작성