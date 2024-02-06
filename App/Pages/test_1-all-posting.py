import pandas as pd
import streamlit as st
from datetime import datetime


path = '../src'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='원티드 채용공고'
)
st.title('원티드 채용공고')
st.write('')

## 데이터프레임 가져오기
try:
    df = pd.read_csv(f'{path}/{now_name}_wanted.csv')
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. Intro 페이지에서 크롤링 실행 버튼을 눌러주세요.')



###########################################################################################



## st.selectbox()

# 빈 값
state = {
    'lab': None,
    'com': None,
    'tit': None,
    'skl': None,
}

# 레이블 선택
lab = st.selectbox(
    '직무',
    ('데이터 분석가', '데이터 사이언티스트'),
    index=None,
    placeholder='직무를 선택해 주세요.'
)
state['lab'] = lab

# 회사 선택
try:
    company_list = list(set(df.loc[df.label == state['lab']].Company.tolist()))
    com = st.selectbox(
        '회사',
        (company_list),
        index=None,
        placeholder='회사를 선택해 주세요.'
    )
    state['com'] = com
except NameError:
    st.error('생성된 파일이 없습니다. Intro 페이지에서 크롤링 실행 버튼을 눌러주세요.')

# 타이틀 선택
try:
    title_list = df.loc[(df.label == state['lab']) & (df.Company == state['com'])].Title.tolist()
    tit = st.selectbox(
        '공고명',
        (title_list),
        index=None,
        placeholder='공고명을 선택해 주세요.'
    )
    state['tit'] = tit
except NameError:
    st.error('생성된 파일이 없습니다. Intro 페이지에서 크롤링 실행 버튼을 눌러주세요.')

# 세부 공고내용 선택
skl = st.selectbox(
    '세부 공고내용',
    ('주요업무', '자격요건', '우대사항'),
    index=None,
    placeholder='보고싶은 세부 공고내용을 선택해 주세요.'
)
state['skl'] = skl
st.write('')

# st.button()
if st.button('확인'):
    cond = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])]
    # 주요업무 선택 시
    if state['skl'] == '주요업무':
        st.write('')
        st.text(cond.Content_0.tolist()[0])
        st.write('')
        link_click = cond.Link.tolist()[0]
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{link_click}]({link_click})')

    # 자격요건 선택 시
    if state['skl'] == '자격요건':
        st.write('')
        st.text(cond.Content_1.tolist()[0])
        st.write('')
        link_click = cond.Link.tolist()
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{link_click}]({link_click})')

    # 우대사항 선택 시
    if state['skl'] == '우대사항':
        st.write('')
        st.text(cond.Content_2.tolist()[0])
        st.write('')
        link_click = cond.Link.tolist()
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{link_click}]({link_click})')