<<<<<<< HEAD
import openai
import time
import pandas as pd
import streamlit as st
import time
import json
import os
from datetime import datetime
from collections import Counter

path = './Data'

now = datetime.now()
now_name = now.strftime('%Y%m%d')
csv_file = f'{path}/{now_name}_major.csv'

# 결과 데이터 파일 경로 설정
result_data_path = f'{path}/{now_name}_result.json'

## page setting
st.set_page_config(
    page_title='Major Company feature'
)
st.title('Major Company feature')
st.write('')


try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. ALL Posting 페이지에서 크롤링 실행 버튼을 눌러주세요.')


# OpenAI API 키 입력 섹션
st.write("""
### API 키 입력
""", unsafe_allow_html=True)
ORGANIZATION_ID = st.text_input('Organization ID 입력:')
OPENAI_API_KEY = st.text_input('OpenAI API 키 입력:', type="password")

# API 키 저장 및 확인 버튼
if 'api_key_valid' not in st.session_state:
    st.session_state['api_key_valid'] = False  # API 키 유효성 상태 플래그

if st.button('적용'):
    try:
        # OpenAI 라이브러리를 사용하여 API 키 설정
        openai.api_key = OPENAI_API_KEY

        # 간단한 요청으로 키 검증 (예: 리스트 엔진)
        response = openai.Engine.list()

        # 성공 메시지 표시
        st.success('API 키가 유효합니다.')
        st.session_state['api_key_valid'] = True
    except Exception as e:
        # 오류 메시지 표시
        st.error(f'API 키 검증 실패: {e}')

# 결과 데이터 로드 또는 생성 함수
def load_or_process_data():
    # 이전에 처리된 데이터가 있는지 확인
    if os.path.exists(result_data_path):
        with open(result_data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['certifications'], data['development_environments'], data['programming_languages']
    else:
                
        def extract_information_with_openai(content, model="gpt-3.5-turbo-1106", max_tokens=100, verbose=False):
            openai.api_key = OPENAI_API_KEY
            prompt = f"""
            Extract and categorize the information from the following job posting into separate lists for certifications, development environments, and programming languages.
            List each category with its items, separated by new lines. Avoid using special characters.
            If there is no information for a category, mention 'No mention' for that category.
            Here are some examples for each category:

            Certifications: 정보처리기사, ADSP, SQLD, 빅데이터분석기사
            Development Environments: Docker, Google Cloud Platform
            Programming Languages: Python, SQL, C, Java

            Job Posting: {content}
            """

            time_start = time.time()
            retry_count = 3
            wait_times = [8, 16, 32]  # 재시도 대기 시간 (초)
            for i in range(retry_count):
                try:
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "system", "content": prompt}],
                        max_tokens=max_tokens
                    )
                    answer = response.choices[0].message["content"].strip()
                    tokens = response.usage.total_tokens

                    time_end = time.time()

                    if verbose:
                        st.write(f'prompt: {prompt} | tokens: {tokens} | {time_end - time_start:.1f}sec\nanswer: {answer}')
                    return answer

                except Exception as error:
                    st.write(f"API Error: {error}")
                    wait_time = 60 * wait_times[i]  # 점진적으로 대기 시간 증가
                    st.write(f"Retrying {i + 1} time(s) in {wait_time} seconds...")

                    if i + 1 == retry_count:
                        return content, None, None
                    time.sleep(wait_time)



        # 데이터 프레임의 각 행에 대한 반복 처리
        for content in df['Content']:
            extracted_text = extract_information_with_openai(content)

            for line in extracted_text.split('\n'):
                if 'Certifications:' in line:
                    current_list = certifications
                elif 'Development Environments:' in line:
                    current_list = development_environments
                elif 'Programming Languages:' in line:
                    current_list = programming_languages
                elif current_list is not None:
                    if line.strip() != '- No mention':
                        current_list.append(line.strip())

        # 결과 데이터 저장
        with open(result_data_path, 'w', encoding='utf-8') as file:
            json.dump({
                'certifications': certifications,
                'development_environments': development_environments,
                'programming_languages': programming_languages
            }, file)

        return certifications, development_environments, programming_languages

# 결과를 각 항목별 리스트로 분리
certifications, development_environments, programming_languages, tools = [], [], [], []
current_list = None

# 데이터 로드 또는 처리
if st.session_state['api_key_valid']:
    certifications, development_environments, programming_languages = load_or_process_data()

def get_top_items(items_list):
    filtered_items = [item for item in items_list if item not in ['- No mention', 'No mention', '', ' ']]
    counter = Counter(filtered_items)
    return counter.most_common(5)

# 상위 5개 항목을 순위별로 포맷팅하는 함수
def format_top_items(items_list):
    if not items_list or all(item in ['- No mention', 'No mention', '', ' '] for item in items_list):
        return ' '
    top_items = get_top_items(items_list)
    formatted_list = [f"{i+1}. {item[0]}" for i, item in enumerate(top_items)]
    return "\n".join(formatted_list)

# Streamlit 컬럼 설정
col1, col2, col3 = st.columns(3)

# 각 컬럼에 상위 5개 항목 표시
with col1:
    st.write("선호하는 자격증")
    st.text(format_top_items(certifications))

with col2:
    st.write("선호하는 개발 환경")
    st.text(format_top_items(development_environments))

with col3:
    st.write("선호하는 개발 언어")
    st.text(format_top_items(programming_languages))
st.write('')
st.write('')

## 채용공고 아웃풋
def posting_output(df, posting):
    IDX = df.loc[df.label == f'{posting}'].index.tolist()
    st.write(f'#### {posting}')
    st.write('파란색 글씨를 누르면 해당 채용공고로 이동됩니다.')
    for i in IDX:
        st.write(f'{i}. {com_list[i]}, [{tit_list[i]}]({lin_list[i]})')

posting = st.selectbox(
    '직무',
    ('데이터 분석가', '데이터 사이언티스트'),
    index=None,
    placeholder='직무를 선택해 주세요.'
)
st.write('')
try:
    df = pd.read_csv(csv_file)
    com_list = df.Company.tolist()
    tit_list = df.Title.tolist()
    lin_list = df.Link.tolist()

    if posting == '데이터 분석가':
        posting_output(df, posting)
    if posting == '데이터 사이언티스트':
        posting_output(df, posting)
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. ALL Posting 페이지에서 크롤링 실행 버튼을 눌러주세요.')
=======
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
>>>>>>> upstream/main
