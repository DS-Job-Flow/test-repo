import streamlit as st

# 스트림릿 페이지 설정
st.title('DS 커리어 분석')

st.markdown('---')

# 스트림릿 사용 방법 링크 제공
st.write("""
### 스트림릿 사용 방법
""", unsafe_allow_html=True)
st.write('이 페이지를 활용하는 방법에 대해 알아보려면 [해당 링크](https://balanced-park-5a8.notion.site/c2f2b1a1677a464b8d80e225d296f803#0a35451ece3a4dc9b9fbf4bdfd92b7b7)를 참조하세요.')

st.write("")
st.write("")
st.write("")

# OpenAI API 키 발급 방법 링크 제공
st.write("""
### OpenAI API 키 발급 방법
""", unsafe_allow_html=True)
st.write('OpenAI API 키 발급 방법에 대해 알아보려면 [해당 링크](https://www.notion.so/API-cd8f03ffd7864dd6bfc4d1dc7b80b0b9)를 참조하세요.')

st.markdown('---')

# 페이지 하단에 추가적인 정보나 안내문구
st.caption('이 페이지는 DS 커리어 분석 페이지의 시작점이며, 사용자가 편리하게 API 키를 입력하고 기본적인 사용 방법을 알 수 있도록 돕습니다.')
