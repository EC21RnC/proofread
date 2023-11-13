import streamlit as st
import openai
from openai import OpenAI
import os
import re
import ast
import json
import streamlit.web.cli as stcli
import pandas as pd




# https://docs.streamlit.io/library/api-reference
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run app.py
# openai.api_key = st.secrets["api_key"]
# os.environ["api_key"] == st.secrets["api_key"]
openai.api_key = os.getenv('api_key')
secret_key = os.getenv('secret_key')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = os.getenv('api_key')
)

# os.environ["api_key"] == st.secrets["api_key"]

# os.environ[]
# ------------------------------------------------------------------- # 
# defs 
# ------------------------------------------------------------------- #

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

import time



# -------------------------------------- #

prompt_naver = \
"""I want you to exract 4 korean keywords out of the given text and make a python list with 3 URLs.
The first keyword should be the country that the text is referring to.
The rest 3 keywords are the most important keywords, that represent the text well.

The output must be only a python list and look like this:

["https://search.naver.com/search.naver?where=news&query=<country>+<keyword 1>+<keyword 2>+<keyword 3>&sm=tab_opt&sort=1", "https://www.google.com/search?q=<country>+<keyword 1>+<keyword 2>+<keyword 3>&tbm=nws", "https://www.google.com/search?q=<country>+<keyword 1>+<keyword 2>+<keyword 3>+site:emerics.org"]"""


def gpt_get_keywords(user_input):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature = 0,
        max_tokens = 300,
        messages=[
            {
                "role": "system",
                "content": prompt_naver
            },
            {
              "role": "user",
              "content": "턔국 상원의원, 전진당에 왕실모독죄 개정 공약을 포기하라고 촉구\n☐ 태국 상원의원이 전진당(Move Forward Party)에 왕실모독죄 개정 공악을 표기하라고 축구함\n- 7월 31일 완차이 손시리(Wanchai Sonsiri) 상원의원은 전진당이 왕실모독죄 개정 공약을 포기한다면, 연정 파트너인 푸어타이(Pheu Thai)당 후보가 신임 총리가 되는데 필요한 상하원 과반수를 확보할 수 있다고 주장함\n- 완차이 손시리 의원은 7월 13일 1차 투표 때 피타 림짜른랏(Pita Limjaroenrat) 전진당 대표에 투표한 상원의원 13명 중 한 사람임\n\n☐ 피타 림짜른랏 전진당 대표가 2차 투표에 참여하지 못하게 되자, 전진당은 차기 정부 구성을 연정 파트너인 푸어타이당에 넘긴 상태임\n- 이에 푸어타이당은 8월 4일로 예정된 2차 투표에서 탁신 전 총리와 가까운 부동산 재벌 스레타 타위신(Srettha Thavisin)을 총리 후보로 지명할 계획임\n- 완차이 손시리 의원은 “푸어타이당이 스레타 타위신을 지명한다면 그에게 표를 던질 것”이라고 덧붙임\n\n☐ 완차이 손시리 의원은 푸어타이당이 다양한 정당 및 상원의원들과 협력할 수 있기 때문에 연립정부를 이끌 가능성이 더 높다고 평가함\n- 완차이 손시리 의원은 “만약 푸어타이당과 전진당이 연립정부 구성에 서로 관심이 없을 경우 전진당이 왕실모독죄 개정 공약을 포기해야만 상원의원들의 지지를 얻을 수 있을 것”이라고 주장함\n- 태국 군부 및 보수파 의원들은 국왕과 왕실을 모독하는 자를 처벌하는 내용을 담은 왕실모독죄 조항을 개정하자는 전진당의 형사법 개혁에 반대하고 있음"
            },
            {
              "role": "assistant",
              "content": "[\"https://search.naver.com/search.naver?where=news&query=태국+전진당+왕실모독죄+푸어타이당&sm=tab_opt&sort=1\", \"https://www.google.com/search?q=태국+전진당+왕실모독죄+푸어타이당&tbm=nws\", \"https://www.google.com/search?q=태국+전진당+왕실모독죄+푸어타이당+site:emerics.org\"]"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return completion.choices[0].message.content

def gpt_get_pnouns(user_input):
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
        "role": "system",
        "content": "제공된 텍스트에서 괄호 안 영어와 함께 표기된 모든 고유명사(기관명, 인물명, 지역명, 정책명, 정당명 등등)를 추출해서 다음과 같은 jason object를 만들어 주세요:\n\n```json\n[\n    {\n        \"순번\": 1,\n        \"한글표기\": \"<한글표기1>\",\n        \"영어표기\": \"<영어표기1>\",\n        \"해당국가\": \"<해당국가1>\",\n        \"이머릭스\": \"https://www.google.com/search?q=<영어표기1>+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=<해당국가1>+<영어표기1>&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=<해당국가1>+<영어표기1>&tbm=nws\"\n    },\n    {\n        \"순번\": 2>,\n        \"한글표기\": \"<한글표기1>\",\n        \"영어표기\": \"<영어표기1>\",\n        \"해당국가\": \"<해당국가1>\",\n        \"이머릭스\": \"https://www.google.com/search?q=<영어표기1>+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=<해당국가1>+<영어표기1>&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=<해당국가1>+<영어표기1>&tbm=nws\"\n    }\n]\n```"
        },
        {
        "role": "user",
        "content": "턔국 상원의원, 전진당에 왕실모독죄 개정 공약을 포기하라고 촉구\n☐ 태국 상원의원이 전진당(Move Forward Party)에 왕실모독죄 개정 공악을 표기하라고 축구함\n- 7월 31일 완차이 손시리(Wanchai Sonsiri) 상원의원은 전진당이 왕실모독죄 개정 공약을 포기한다면, 연정 파트너인 푸어타이(Pheu Thai)당 후보가 신임 총리가 되는데 필요한 상하원 과반수를 확보할 수 있다고 주장함\n- 완차이 손시리 의원은 7월 13일 1차 투표 때 피타 림짜른랏(Pita Limjaroenrat) 전진당 대표에 투표한 상원의원 13명 중 한 사람임\n\n☐ 피타 림짜른랏 전진당 대표가 2차 투표에 참여하지 못하게 되자, 전진당은 차기 정부 구성을 연정 파트너인 푸어타이당에 넘긴 상태임\n- 이에 푸어타이당은 8월 4일로 예정된 2차 투표에서 탁신 전 총리와 가까운 부동산 재벌 스레타 타위신(Srettha Thavisin)을 총리 후보로 지명할 계획임\n- 완차이 손시리 의원은 “푸어타이당이 스레타 타위신을 지명한다면 그에게 표를 던질 것”이라고 덧붙임\n\n☐ 완차이 손시리 의원은 푸어타이당이 다양한 정당 및 상원의원들과 협력할 수 있기 때문에 연립정부를 이끌 가능성이 더 높다고 평가함\n- 완차이 손시리 의원은 “만약 푸어타이당과 전진당이 연립정부 구성에 서로 관심이 없을 경우 전진당이 왕실모독죄 개정 공약을 포기해야만 상원의원들의 지지를 얻을 수 있을 것”이라고 주장함\n- 태국 군부 및 보수파 의원들은 국왕과 왕실을 모독하는 자를 처벌하는 내용을 담은 왕실모독죄 조항을 개정하자는 전진당의 형사법 개혁에 반대하고 있음"
        },
        {
        "role": "assistant",
        "content": "[\n    {\n        \"순번\": 1,\n        \"한글표기\": \"완차이 손시리\",\n        \"영어표기\": \"Wanchai Sonsiri\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Wanchai+Sonsiri+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Wanchai+Sonsiri&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Wanchai+Sonsiri&tbm=nws\"\n    },\n    {\n        \"순번\": 2,\n        \"한글표기\": \"전진당\",\n        \"영어표기\": \"Move Forward Party\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Move+Forward+Party+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Move+Forward+Party&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Move+Forward+Party&tbm=nws\"\n    },\n    {\n        \"순번\": 3,\n        \"한글표기\": \"푸어타이당\",\n        \"영어표기\": \"Pheu Thai Party\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Pheu+Thai+Party+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Pheu+Thai+Party&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Pheu+Thai+Party&tbm=nws\"\n    },\n    {\n        \"순번\": 4,\n        \"한글표기\": \"피타 림짜른랏\",\n        \"영어표기\": \"Pita Limjaroenrat\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Pita+Limjaroenrat+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Pita+Limjaroenrat&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Pita+Limjaroenrat&tbm=nws\"\n    },\n    {\n        \"순번\": 5,\n        \"한글표기\": \"스레타 타위신\",\n        \"영어표기\": \"Srettha Thavisin\",\n        \"해당국가\": \"태국\",\n        \"이머릭스\": \"https://www.google.com/search?q=Srettha+Thavisin+site:emerics.org\",\n        \"네이버\": \"https://search.naver.com/search.naver?where=news&query=태국+Srettha+Thavisin&sm=tab_opt&sort=1\",\n        \"구글\": \"https://www.google.com/search?q=태국+Srettha+Thavisin&tbm=nws\"\"\n    }\n\n]"
        },
        {
        "role" : "user",
        'content' : user_input
            
        }
    ],
    temperature=0,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )
    return response.choices[0].message.content



# ------------------------------------------------------------------- #
import streamlit as st
st.set_page_config( layout = 'wide' )

tab1, tab2 = st.tabs(["검사", "히스토리"])

# Initialize the history in the session state
if "history" not in st.session_state:
    st.session_state["history"] = []



# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
#
# setting
#

with tab1:
    

    #
    # Title
    #
    st.title(":blue[EC21R&C] Proof Reader")
    st.divider()
    #
    #
    #

    secret_key_user = st.text_input(':secret: **Secret Key**', placeholder = 'chan@ec21rnc.com에 문의해주세요')

    #
    # 0. 글 입력
    #

    st.header(':page_with_curl:글 입력')
    # with st.form("proofread"):
    placeholder = """[검수 대상 텍스트 입력]"""
    with st.form("input_text"):
        st.subheader('뉴스브리핑')
        user_input = st.text_area("_한글로 작성된 요약본을 의미해요_", placeholder = placeholder, height = 500)
        submit = st.form_submit_button("**:fast_forward: 검사시작**", use_container_width = True)

     

    st.divider()
    # submit_summary = st.form_submit_button(":printer: **팩트체크시작** :printer:", use_container_width = True)

    st.header(':page_with_curl: 검사결과')

    #
    # 맞춤법검사 ()
    #

    # html = ""
    if submit and user_input and len(user_input) < 2000 and secret_key == secret_key_user:

        with st.spinner("_:robot_face: GPT가 고유명사를 찾고 있어요..._"):
            result_proper = gpt_get_pnouns(user_input)
            result_proper = pd.DataFrame(json.loads(result_proper))
            st.subheader('>> 고유명사 검색 결과')
            with st.expander('펼쳐서 보기'):
                st.dataframe(result_proper,
                             column_config={'이머릭스' : st.column_config.LinkColumn('이머릭스 링크'),
                                                       '네이버' : st.column_config.LinkColumn('네이버 링크'),
                                                       '구글' : st.column_config.LinkColumn('구글 링크')
                                           }
                            )


        st.divider()

        with st.spinner("GPT가 관련된 기사를 찾아보고 있어요..."):
            html_list = gpt_get_keywords(user_input)
            html_list = ast.literal_eval(html_list)

            st.subheader('>> 관련기사 검색 결과')
            st.markdown(html_list[0])
            st.markdown(html_list[1])
            st.markdown(html_list[2])

        
    elif user_input and len(user_input) > 2000 and submit:
        st.error('2000자 미만으로 입력하세요...' + '→ `현재 글자수 : {}`'.format( str(len(user_input))), icon="🚨")
    elif user_input and len(user_input) == 0 and submit:
        st.error('뉴스브리핑을 입력하세요', icon="🚨")
    elif user_input and len(user_input) != 0 and submit and len(secret_key_user) != 0 and secret_key != secret_key_user:
        st.error('올바른 `Secret Key`를 입력하세요', icon="🚨")
    elif user_input and len(user_input) != 0 and submit and len(secret_key_user) == 0:
        st.error('`Secret Key`를 입력하세요', icon="🚨")
    else:
        pass

st.divider()
# Append items to history as a list
if submit and user_input and secret_key == secret_key_user:
    st.session_state["history"].append([user_input, result_proper, html_list[0], html_list[1], html_list[2]])



# Display history
with tab2:
    st.markdown('#  :speech_balloon: History')
    st.caption(':warning: 페이지를 새로고침하면 히스토리가 사라집니다')
    if submit and user_input and secret_key == secret_key_user:
        for i, item in enumerate(st.session_state["history"]):
            with st.expander(item[0].split('\n')[0].strip()):
                st.subheader('뉴스브리핑')
                st.code(item[0], language = 'markdown')
                
                st.subheader('고유명사')
                st.dataframe(item[1],
                             column_config={'이머릭스' : st.column_config.LinkColumn('이머릭스 링크'),
                                                       '네이버' : st.column_config.LinkColumn('네이버 링크'),
                                                       '구글' : st.column_config.LinkColumn('구글 링크')
                                           })
                
                st.subheader('기사검색결과')
                st.code(item[2] + '\n' + item[3] + '\n' + item[4], language = 'markdown')


    st.markdown('---')


    #
    #
    #
