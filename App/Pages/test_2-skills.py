import time
import pandas as pd
import streamlit as st
from datetime import datetime
from openai import OpenAI


path = './Data'

now = datetime.now()
now_name = now.strftime('%Y%m%d')
csv_file = f'{path}/{now_name}.csv'


## page setting
st.set_page_config(
    page_title='Skills'
)
st.title('Skills')
st.write('')


try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. ALL Posting 페이지에서 크롤링 실행 버튼을 눌러주세요.')


## OpenAI API
ORGANIZATION_ID = 'org-xxx' # 개인 ID 필요
OPENAI_API_KEY = 'sk-xxx' # 개인 API KEY 필요
client = OpenAI(
    organization = ORGANIZATION_ID,
    api_key = OPENAI_API_KEY
)


## 주어진 프롬프트에 대한 응답을 생성하는 함수
def get_completion(prompt, model="gpt-3.5-turbo-1106", temperature=0, verbose=False):
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
    company_list = df.loc[df.label == state['lab']].Company.tolist()
    com = st.selectbox(
        '회사',
        (company_list),
        index=None,
        placeholder='회사를 선택해 주세요.'
    )
    state['com'] = com
except NameError:
    st.error('생성된 파일이 없습니다. ALL Posting 페이지에서 크롤링 실행 버튼을 눌러주세요.')

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
    st.error('생성된 파일이 없습니다. ALL Posting 페이지에서 크롤링 실행 버튼을 눌러주세요.')
    
# 역량 선택
skl = st.selectbox(
    '역량',
    ('자격요건', '우대사항', '개발환경'),
    index=None,
    placeholder='보고싶은 역량을 선택해 주세요.'
)
state['skl'] = skl

st.write('')
if st.button('확인'):
    # 자격요건 선택 시
    if state['skl'] == '자격요건':        
        # 응답 생성 함수 실행
        st_info = st.info('gpt-3.5-turbo-1106 실행 중')
        text = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Content.tolist()[0]
        prompt = f"""
        You will be provided with text delimited by triple quotes.
        
        The text is structured "... - 주요업무 - 자격요건 - 우대사항 - ... - 기술스택 ・ 툴"
        The order of the structure may change and there may be no one or more of the elements of the structure.

        Please extract the content corresponding to "\n자격요건\n".

        Write those instructions in the following format: \
        - ...

        If the text does not contain a "\n자격요건\n", \
        then simply write \"None.\"
        
        Be careful not to print out a prompt.
        \"\"\"{text}\"\"\"
        """
        # 응답 반환
        response = get_completion(prompt)
        
        time.sleep(1)
        st_info.empty()
        st_success = st.success('gpt-3.5-turbo-1106 실행 완료')
        time.sleep(1)
        st_success.empty()

        st.markdown('---')
        st.write(response)

        wonder_link = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Link.tolist()
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{wonder_link[0]}]({wonder_link[0]})')

    # 우대사항 선택 시
    elif state['skl'] == '우대사항':
        # 응답 생성 함수 실행
        st_info = st.info('gpt-3.5-turbo-1106 실행 중')
        text = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Content.tolist()[0]
        prompt = f"""
        You will be provided with text delimited by triple quotes.
        
        The text is structured "... - 주요업무 - 자격요건 - 우대사항 - ... - 기술스택 ・ 툴"
        The order of the structure may change and there may be no one or more of the elements of the structure.
        
        Please extract the content corresponding to "\n우대사항\n".

        Write those instructions in the following format: \
        - ...    

        If the text does not contain a "\n우대사항\n", \
        then simply write \"None.\"

        Be careful not to print out a prompt.
        \"\"\"{text}\"\"\"
        """
        # 응답 반환
        response = get_completion(prompt)
        
        time.sleep(1)
        st_info.empty()
        st_success = st.success('gpt-3.5-turbo-1106 실행 완료')
        time.sleep(1)
        st_success.empty()

        st.markdown('---')
        st.write(response)

        wonder_link = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Link.tolist()
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{wonder_link[0]}]({wonder_link[0]})')

    # 개발환경 선택 시
    elif state['skl'] == '개발환경':
        # 응답 생성 함수 실행
        st_info = st.info('gpt-3.5-turbo-1106 실행 중')
        text = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Content.tolist()[0]
        prompt = f"""
        You will be provided with text delimited by triple quotes.
        
        The text is structured "... - 주요업무 - 자격요건 - 우대사항 - ... - 기술스택 ・ 툴"
        The order of the structure may change and there may be no one or more of the elements of the structure.
        
        Please extract the content corresponding to "\n기술스택 ・ 툴\n".  

        Write those instructions in the following format: \
        - ...

        If the text does not contain a "\n기술스택 ・ 툴\n", \
        please extract the content corresponding to development environment such as Language, Framework, Tool, etc..
        
        Be careful not to print out a prompt.
        \"\"\"{text}\"\"\"
        """
        # 응답 반환
        response = get_completion(prompt)
        
        time.sleep(1)
        st_info.empty()
        st_success = st.success('gpt-3.5-turbo-1106 실행 완료')
        time.sleep(1)
        st_success.empty()

        st.write('---')
        st.write(response)

        wonder_link = df.loc[(df.label == state['lab']) & (df.Company == state['com']) & (df.Title == state['tit'])].Link.tolist()
        st.write(f'채용정보가 더 궁금하다면 링크 클릭! 👉 [{wonder_link[0]}]({wonder_link[0]})')