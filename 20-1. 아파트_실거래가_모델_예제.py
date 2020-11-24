# -*- coding: utf-8 -*-
import pandas as pd

# data 읽기
# 로컬 환경에서는 colab과 경로가 다릅니다. 

# data = pd.read_csv('C:/Users/jooho_temp/Documents/AptPrice/아파트(매매)__실거래가_20200919105434.csv', encoding='cp949',
#                    skiprows = 15)  #skiprows 옵션을 통해 불필요한 행을 건너뛸수 있습니다

data = pd.read_csv('아파트(매매)__실거래가_20200919105434.csv', encoding='cp949',
                   skiprows = 15)  #skiprows 옵션을 통해 불필요한 행을 건너뛸수 있습니다


# 문자로 인식된 것을 숫자로 바꾼다. 그러려면 ,를 먼저 삭제해야 한다
data['거래금액(만원)'] = data['거래금액(만원)'].str.replace(',','')
data['거래금액(만원)'] = data['거래금액(만원)'].astype('int')

# 비교를 위해 평당가격을 계산한다. 
df = data.assign(평당단가 = data['거래금액(만원)']/data['전용면적(㎡)'])

### 경기도 안양시 분석

# 안양시 선택
안양 = df.시군구.str.contains('안양동안구')
print(안양)

anyang_df = df[안양]

# 경기도 안양시 이외에 안양이 들어간 곳이 있는 확인
anyang_df.시군구.unique()

# 분석에 활용할 데이터만 선택
anyang_df = anyang_df.filter(['층','건축년도','전용면적(㎡)','평당단가'])
anyang_df = anyang_df.rename(columns={'전용면적(㎡)':'전용면적'})

"""* seaborn pairplot으로 요소들의 관계를 살펴봅시다"""
 
# 로컬 환경에서 matplotlib 한글 처리 
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

import seaborn as sns
sns.pairplot(anyang_df)

import statsmodels.formula.api as smf

# 평당단가와 층, 건축년도, 전용면적의 모델을 만들어보자
lm = smf.ols(formula='평당단가 ~ 층+건축년도+전용면적', data=anyang_df).fit()
lm.summary() # 기본적인 통계치 출력

def predict(model):
    층 = float(input('선호하는 층을 입력하세요 >> '))
    건축년도 = float(input('선호하는 건축년도를 입력하세요 >> '))
    전용면적 = float(input('선호하는 전용면적(m**2)을 입력하세요 >> '))
    data = {'층':층, '건축년도':건축년도, '전용면적':전용면적}
    p=model.predict(data)
    print('예상 평당단가(m**2)는 {:,.2f}만원입니다.'.format(p[0]))
    print('예상 가격은  {:,.2f}억원입니다. '.format((전용면적 * p[0])/10000))

p = predict(lm)

print("model")
print("평당단가 = {:.2f} + {:.2f}*층 + {:.2f}*건축년도 + {:.2f}* 전용면적".format(lm.params.Intercept, lm.params.층, lm.params.건축년도, lm.params.전용면적))

