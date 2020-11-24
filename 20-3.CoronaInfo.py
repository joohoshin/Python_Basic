import pandas as pd
import streamlit as st

raw_df = pd.read_csv('https://raw.githubusercontent.com/joohoshin/Python_Basic/master/coronainfo.csv', index_col=0)

raw_df = raw_df.set_index('기준일')
raw_df = raw_df.rename(columns = {'사망자수':'누적사망자수', '확진자수':'누적확진자수'})
cols = ['치료중환자수', '누적사망자수', '누적확진자수', '검사진행수']
df = raw_df[cols]
df = df.dropna()
df = df.sort_index(ascending = True)


st.title('코로나 국내 현황')

# 로컬 환경에서 matplotlib 한글 처리 
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

option = st.selectbox('차트를 선택하세요', cols)
df_chart = df[option]
st.subheader(option)
df_chart.plot()
st.pyplot()