import os
import time
import openai
import pandas as pd
import streamlit as st
from datetime import datetime
from glob import glob
from openai import OpenAI


path = '../src'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='채용공고 요약 결과 확인'
)
st.title('채용공고 요약 결과 확인')
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



## 주어진 프롬프트에 대한 응답을 생성하는 함수
def get_completion(prompt, model="gpt-3.5-turbo-0125", temperature=0, verbose=False):
    messages = [{"role": "user", "content": prompt}]

    time_start = time.time()
    retry_count = 3
    wait_times = [8, 16, 32]
    for i in range(0, retry_count):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            answer = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens

            time_end = time.time()

            if verbose:
                st.write('prompt: %s | token: %d | %.1fsec\nanswer : %s' % (prompt, tokens, (time_end - time_start), answer))
            return answer

        except Exception as error:
            st.write(f"API Error: {error}")
            wait_time = 60 * wait_times[i]  # 점진적으로 대기 시간을 증가
            st.write(f"Retrying {i+1} time(s) in {wait_time} seconds...")

            if i+1 == retry_count:
                return prompt, None, None
            time.sleep(wait_time)



###########################################################################################



## 문장 요약 프롬프트
def summary_prompt(data, lab, skl):

    if skl == '자격요건':
        p_skl = 'Content_1'
    elif skl == '우대사항':
        p_skl = 'Content_2'

    data = df.loc[df.label == f'{lab}', f'{p_skl}'].tolist()
    cond = 0
    L = []

    st_info = st.info('문장 요약 중')
    while cond < len(data):
        text = data[cond:cond+10]

        prompt = f"""
        세 개의 따옴표로 구분된 텍스트가 제공됩니다.
        이 텍스트는 {lab}의 채용공고들로, 공고 내용 중 {skl}만 추출하였습니다.
        이 텍스트 정보를 통해, {lab}의 {skl}를 요약해주세요.
        생성 형식은 다음과 같습니다.
        - ...
        - ...
        - ...

        프롬프트를 출력하지 않도록 주의하십시오.
        \"\"\"{text}\"\"\"
        """
        # 응답 반환
        response = get_completion(prompt)
        L.append(response)

        cond += 10

    st_info.empty()
    st_success = st.success('문장 요약 완료')
    time.sleep(1)
    st_success.empty()


    return L



###########################################################################################
    


## st.selectbox()
# 빈 값
state = {
    'plf': None,
    'lab': None,
    'skl': None,
}

# 플랫폼 선택
plf = st.selectbox(
    '플랫폼',
    ('원티드', 'None'),
    index=None,
    placeholder='플랫폼을 선택해 주세요.'
)
state['plf'] = plf

# 원티드 선택 시
if state['plf'] == '원티드':

    # 레이블 선택
    lab = st.selectbox(
        '직무',
        ('데이터 분석가', '데이터 사이언티스트'),
        index=None,
        placeholder='직무를 선택해 주세요.'
    )
    state['lab'] = lab
        
    # 세부 공고내용 선택
    skl = st.selectbox(
        '세부 공고내용',
        ('자격요건', '우대사항'),
        index=None,
        placeholder='보고싶은 세부 공고내용을 선택해 주세요.'
    )
    state['skl'] = skl
    st.write('')

    # st.button()
    if st.button('확인'):

        # 문장 요약 파일이 없으면
        # 파일 제거
        if not os.path.exists(f'{path}/{now_name}_wanted_{state["lab"]}_{state["skl"]}_summary.txt'):
            files_del = glob(f'{path}/*_wanted_{state["lab"]}_{state["skl"]}_summary.txt')
            for file_del in files_del:
                os.remove(file_del)
            generate = summary_prompt(df, state['lab'], state['skl'])
            g_join_split = ','.join(generate)

            # 문장 요약 저장
            with open(f'{path}/{now_name}_wanted_{state["lab"]}_{state["skl"]}_summary.txt', 'w', encoding='utf-8') as file:
                file.write(g_join_split)
            st.write('')
            st.text(g_join_split)

        # 문장 요약 파일이 있으면
        else:
            st_info = st.info('생성된 파일이 있습니다.')
            time.sleep(1)
            st_info.empty()

            # 문장 요약 불러오기
            with open(f'{path}/{now_name}_wanted_{state["lab"]}_{state["skl"]}_summary.txt', 'r', encoding='utf-8') as file:
                g_join_split = file.read()
            st.write('')
            st.text(g_join_split)

        # 추가 사항
        # 1. 문장 유사도 분석 (코사인 유사도)
        # 2. 높은 유사도를 가지는 문장끼리 모아서 프롬프트를 사용해 한 문장으로 요약
        # 3. 출력 (st.text(g_join_split)는 삭제해야 됨)

# None 선택 시
if state['plf'] == 'None':
    pass