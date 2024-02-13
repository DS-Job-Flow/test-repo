import pandas as pd
import streamlit as st
from datetime import datetime


path = '../src'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='채용공고 확인'
)
st.title('채용공고 확인')
st.write('')

<<<<<<< HEAD
def make_dict():
    data_wanted = {'Lin': [], 'Tit': [], 'Com': [], 'Loc': [], 'Ctn': []}
    data_saramin = {'Lin': [], 'Tit': [], 'Com': [], 'Loc': [], 'Ctn': []}
    data_major = {'Lin': [], 'Tit': [], 'Com': [], 'Loc': [], 'Ctn': []}

    return data_wanted, data_saramin, data_major

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
def Wanted(KEYWORD, data_wanted):

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(f'https://www.wanted.co.kr/search?query={KEYWORD}&tab=position')
    driver.implicitly_wait(2)
    scroll(driver)

    # 검색 키워드 출력
    print(f'\n\n##### {KEYWORD} #####')
    
    # 공고 개수
    num = driver.find_element(By.XPATH, '//*[@id="search_tabpanel_position"]/div/div[1]/h2').text
    num = int(num.replace('포지션', ''))
    for i in range(1, num+1):
        try:
            # 링크
            p_0 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a').get_attribute('href')
            data_wanted['Lin'].append(p_0)                       

            # 타이틀
            p_1 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/strong').text
            data_wanted['Tit'].append(p_1)

            # 회사
            p_2 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/span[1]/span[1]').text
            data_wanted['Com'].append(p_2)                       

            # 위치
            p_3 = driver.find_element(By.XPATH, f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{i}]/a/div[2]/span[1]/span[2]').text
            data_wanted['Loc'].append(p_3)                    
        except Exception as e:
            st.write(e)
            break

    # 데이터 출력
    elem_return_0('링크', data_wanted['Lin'])
    elem_return_0('타이틀', data_wanted['Tit'])
    elem_return_0('회사', data_wanted['Com'])
    elem_return_0('위치', data_wanted['Loc'])

    for i in data_wanted['Lin']:
        driver.get(i)
        driver.implicitly_wait(2)
        scroll_one(driver)

        # 공고내용
        try:
            p_4 = driver.find_element(By.CLASS_NAME, 'JobDescription_JobDescription__VWfcb').text
            data_wanted['Ctn'].append(p_4)
        except Exception as e:
            st.write(e)
            break

    driver.close()

    # 데이터 출력
    elem_return_1('공고내용', data_wanted['Ctn'])

    # 데이터프레임 생성
    df_wanted = pd.DataFrame({
        'Title' : data_wanted['Tit'],
        'Company' : data_wanted['Com'],
        'Content' : data_wanted['Ctn'],   
        'Link' : data_wanted['Lin'],
        'Location' : data_wanted['Loc'],
        'label' : f'{KEYWORD}'         
    })
<<<<<<< HEAD
=======

>>>>>>> ce67bb00ce720aa80ebf23f919faf98329d2fd60
    keyword_csv_file = f'{path}/{KEYWORD}_wanted.csv'
    df_wanted.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')
    df_wanted = pd.read_csv(keyword_csv_file)
    
    return data_wanted
<<<<<<< HEAD
=======

    keyword_csv_file = f'{path}/{KEYWORD}.csv'
    df.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')

    return data

>>>>>>> ce67bb00ce720aa80ebf23f919faf98329d2fd60

## 사람인, 대기업 수집
def Saramin_logic(front_url, mid_url, back_url, page, data):

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(front_url+KEYWORD+mid_url+str(page)+back_url)
    driver.implicitly_wait(2)
    
    # keyword 채용공고 확인 후 전체 페이지 수
    ct_result = driver.find_element(By.XPATH, '//*[@id="recruit_info"]/div[1]/span').text
    total_result = re.sub(r'[^0-9]', '', ct_result)
    page_ct = int(int(total_result)/100)

    # 검색 키워드 출력
    print(f'\n\n##### {KEYWORD} #####')

    # 공고 개수
    for pages in range(1, page_ct+2):
        try:
            driver.get(front_url+KEYWORD+mid_url+str(pages)+back_url)
            driver.implicitly_wait(2)

            div_1 = driver.find_elements(By.CLASS_NAME, "job_tit")
            for item in div_1:
                
                #링크
                p_0 = item.find_element(By.TAG_NAME, "a").get_attribute('href')
                data['Lin'].append(p_0)

                #타이틀
                p_1 = item.find_element(By.TAG_NAME, "a").text
                data['Tit'].append(p_1)

            # 회사
            div_2 = driver.find_elements(By.CLASS_NAME, "item_recruit")
            for item in div_2:
                p_2 = item.find_element(By.TAG_NAME, "a").text
                data['Com'].append(p_2)
            
            #위치
            div_3 = driver.find_elements(By.CLASS_NAME, "job_condition")
            for item in div_3:
                tmp_loc = item.find_element(By.TAG_NAME, "a").text
                p_3 = tmp_loc[:2]
                data['Loc'].append(p_3)
             
            # 데이터 출력
            elem_return_0('링크', data['Lin'])
            elem_return_0('타이틀', data['Tit'])
            elem_return_0('회사', data['Com'])
            elem_return_0('위치', data['Loc'])

        except Exception as e:
            st.write(e)
            break

    return data

## 사람인 수집
def Saramin(KEYWORD, data_saramin):
    
    page = 1

    front_url = 'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword='
    mid_url = '&recruitPage='
    back_url = '&recruitSort=relation&recruitPageCount=100&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&show_applied=&quick_apply=n&except_read=n&ai_head_hunting=n&mainSearch=y'

    data_saramin = Saramin_logic(front_url, mid_url, back_url, page, data_saramin)

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    for i in data_saramin['Lin']:
        driver.get(i)
        driver.implicitly_wait(2)
        scroll_one(driver)

        # 공고내용
        try:
            driver.switch_to.frame("iframe_content_0")
            p_4 = driver.find_element(By.CLASS_NAME, "user_content").text
            data_saramin['Ctn'].append(p_4)

        except Exception as e:
            st.write(e)
            break

    driver.close()

    # 데이터 출력
    elem_return_1('공고내용', data_saramin['Ctn'])

        # 데이터프레임 생성
    df_saramin = pd.DataFrame({
        'Title' : data_saramin['Tit'],
        'Company' : data_saramin['Com'],
        'Content' : data_saramin['Ctn'],   
        'Link' : data_saramin['Lin'],
        'Location' : data_saramin['Loc'],
        'label' : f'{KEYWORD}'         
    })

    keyword_csv_file = f'{path}/{KEYWORD}_saramin.csv'
    df_saramin.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')
    df_saramin = pd.read_csv(keyword_csv_file)

    return data_saramin

## 대기업 수집
def Major(KEYWORD, data_major):

    page = 1

    front_url = 'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword='
    mid_url = '&recruitPage='
    back_url = '&recruitSort=relation&recruitPageCount=100&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&company_type=scale001&show_applied=&quick_apply=n&except_read=n&ai_head_hunting=n&mainSearch=y'

    data_major = Saramin_logic(front_url, mid_url, back_url, page, data_major)

    # webdriver 실행
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    for i in data_major['Lin']:
        driver.get(i)
        driver.implicitly_wait(2)
        scroll_one(driver)

        # 공고내용
        try:
            driver.switch_to.frame("iframe_content_0")
            p_4 = driver.find_element(By.CLASS_NAME, "user_content").text
            data_major['Ctn'].append(p_4)

        except Exception as e:
            st.write(e)
            break

    driver.close()

    # 데이터 출력
    elem_return_1('공고내용', data_major['Ctn'])

        # 데이터프레임 생성
    df_major = pd.DataFrame({
        'Title' : data_major['Tit'],
        'Company' : data_major['Com'],
        'Content' : data_major['Ctn'],   
        'Link' : data_major['Lin'],
        'Location' : data_major['Loc'],
        'label' : f'{KEYWORD}'         
    })

    keyword_csv_file = f'{path}/{KEYWORD}_major.csv'
    df_major.to_csv(keyword_csv_file, index=False, encoding='utf-8-sig')
    df_major = pd.read_csv(keyword_csv_file)

    return data_major

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
now_csv_file_major = f'{path}/{now_name}_major.csv'

# 버튼 클릭
if st.button('크롤링 실행'):
    if not os.path.exists(now_csv_file):
        data_wanted, data_saramin, data_major = make_dict()
        # 크롤링 시작 
        st_info = st.info('크롤링 진행 중')
        for KEYWORD in KEYWORDS:
            data_wanted = Wanted(KEYWORD, data_wanted)
            data_saramin = Saramin(KEYWORD, data_saramin)
            data_major = Major(KEYWORD, data_major)
        

        time.sleep(1)
        st_info.empty()
        st_success = st.success('크롤링 완료')
        time.sleep(1)
        st_success.empty()

        # Data Preprocessing
        # merge
        st_info = st.info('데이터 처리 중')

        DA_major = pd.read_csv(f'{path}/{KEYWORDS[0]}_major.csv')
        DS_major = pd.read_csv(f'{path}/{KEYWORDS[1]}_major.csv')
        df = pd.concat([DA_major, DS_major], axis=0)
        df.to_csv(now_csv_file_major, index=False, encoding='utf-8-sig')
        df = pd.read_csv(now_csv_file_major)

        DA_wanted = pd.read_csv(f'{path}/{KEYWORDS[0]}_wanted.csv')
        DS_wanted = pd.read_csv(f'{path}/{KEYWORDS[1]}_wanted.csv')
        DA_saramin = pd.read_csv(f'{path}/{KEYWORDS[0]}_saramin.csv')
        DS_saramin = pd.read_csv(f'{path}/{KEYWORDS[1]}_saramin.csv')
        df = pd.concat([DA_wanted, DS_wanted, DA_saramin, DS_saramin], axis=0)
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
        os.remove(f'{path}/{KEYWORDS[0]}_major.csv')
        os.remove(f'{path}/{KEYWORDS[1]}_major.csv')
        os.remove(f'{path}/{KEYWORDS[0]}_wanted.csv')
        os.remove(f'{path}/{KEYWORDS[1]}_wanted.csv')
        os.remove(f'{path}/{KEYWORDS[0]}_saramin.csv')
        os.remove(f'{path}/{KEYWORDS[1]}_saramin.csv')
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
=======
## 데이터프레임 가져오기
>>>>>>> upstream/main
try:
    df = pd.read_csv(f'{path}/{now_name}_wanted.csv')
except FileNotFoundError:
    st.error('생성된 파일이 없습니다. Intro 페이지에서 크롤링 실행 버튼을 눌러주세요.')



###########################################################################################



## st.selectbox()

# 빈 값
state = {
    'plf': None,
    'lab': None,
    'com': None,
    'tit': None,
    'skl': None,
}

# 플랫폼 선택
plf = st.selectbox(
    '플랫폼',
    ('원티드', '캐치'),
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

# 캐치 선택 시
if state['plf'] == '캐치':
    pass