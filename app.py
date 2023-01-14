# 전체코드 
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
import re
from bs4 import BeautifulSoup
import urllib.request as req
import streamlit as st
import urllib.parse as par

st.title('BREAKOUT SON')
user_input = st.text_input('본문 또는 URL 입력')

if 'blog.naver.com' in user_input:
    url = user_input

    if not 'm.blog.naver.com' in url:
        url = url.replace('blog.naver.com', 'm.blog.naver.com')

    code = req.urlopen(url)
    soup = BeautifulSoup(code, 'html.parser')

    title = soup.select_one('#SE-b28e8031-860b-4891-9f6b-228ccf1c844f')
    str = soup.select_one('div.se-main-container')
    str = str.text
    # str = str.text.replace('\n', '').strip()
else:
    str = user_input

okt = Okt()
tokenizer = Tokenizer(19417, oov_token = 'OOV')
with open('wordIndex.json') as json_file:
  word_index = json.load(json_file)
  tokenizer.word_index = word_index

loaded_model = load_model('best_model.h5')

# 감성 분류 함수
def sentiment_predict(new_sentence):
    st.write(new_sentence)
    max_len = 30
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    st.write ('긍정감성분석 {:.1f}%'.format(score*100))
    if score <= 0.10:
        st.write ('부정 감성 검토 바랍니다. **************************************************')

# 블로그 에디터 창에서 안보이지만 따라오는 단어들
remove_list = ['대표사진 삭제', '사진 설명을 입력하세요.', '출처 입력', '사진 삭제','이미지 썸네일 삭제', '동영상 정보 상세 보기','동영상 설명을 입력하세요.']

# 따라온 단어들 삭제
for i in remove_list:
    str = str.replace(i, '')

# 문장 단위로 잘라서 감성분석을 해보자
str_phr = str.split('\n')
str_phr = list(filter(None, str_phr))

# 공백과 줄바꿈 삭제
str_re = re.sub('\n| ', '', str)
str_without_line = str.replace('\n','').strip() #줄바꿈만 정리한 것

# 감성분석 전체분석
st.write ('### 전체적 감성 분석결과')
sentiment_predict(str_without_line)


# # 감성분석 부분단위로 분석하는 과정
for i in str_phr:
    if i == ' ':
        continue
    max_len = 30
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    k = okt.morphs(i, stem=True)  # 토큰화
    k = [word for word in k if not word in stopwords]  # 불용어 제거
    encoded = tokenizer.texts_to_sequences([k])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
    score = float(loaded_model.predict(pad_new))  # 예측
    st.wrtie (i)
    st.write('긍정감성분석 {:.1f}%'.format(score * 100))
    if score <= 0.20:
        st.write ('****부정 감성 검토 바랍니다. ****')
