import streamlit as st

from st_pages import add_page_title, add_indentation


import requests

def make_api_request(type,sentence):
    response = requests.get(f"http://localhost:9999/meet/?type={type}&sentence={sentence}")
    return response.json()

add_page_title()
add_indentation()
st.subheader('만들어진 모델을 바탕으로 문장분석을 테스트 해 볼 수 있습니다.')
st.divider()

option = st.selectbox(
    '테스트할 모델을 선택하세요.',
    ('Chanho-Park1.0', 'BeomYun-Kwon1.0'))

st.write('선택된 모델 : ', option)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(":high_brightness: Examples")
    st.markdown("《⭐60분 순삭》 사람들이 잘 모르는 한국영화 띵작!!")
    st.markdown("지난 3월 사전 테스트 당시 가장 크게 느낀 점은 답답함이었다. 전작들에서 몬스터를 마구잡이로 쓸어버리며 느꼈던 시원함은 온데간데없다.")
with col2:
    st.markdown(":zap: Capabilities")
    st.markdown("Remembers what user said earlier in the conversation")
    st.markdown("Allows user to provide follow-up corrections")
    st.markdown("Trained to decline inappropriate requests")
with col3:
    st.markdown(":warning: Limitations")
    st.markdown("May occasionally generate incorrect information")
    st.markdown("May occasionally produce harmful instructions or biased content")
    st.markdown("Limited knowledge of world and events after 2021")

sentence = st.text_input('Movie title','')
st.write('Your sentense is : ',sentence)

if sentence != "":
    if st.button('Test!'):
        #load model, set cache to prevent reloading
        # model = load_model(option)
        
        # model inference, call api
        with st.spinner("Classifying..."):
            result = make_api_request(type=option, sentence=sentence)
            # output = movie_evaluation_predict(model, sentence)
            st.markdown(f" **{result['accuracy']}** 의 정확도로 해당 문장은 **{result['flag']}**입니다.")
            
