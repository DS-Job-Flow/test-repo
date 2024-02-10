import os
import time
import pandas as pd
import streamlit as st
from datetime import datetime


path = '../src'

now = datetime.now()
now_name = now.strftime('%Y%m%d')


## page setting
st.set_page_config(
    page_title='최신 IT 뉴스 모음'
)
st.title('최신 IT 뉴스 모음')
st.write('')