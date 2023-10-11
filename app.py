# ------------------------------------------------------------------- #
import streamlit as st
import openai
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


# https://docs.streamlit.io/library/api-reference
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run app.py
# openai.api_key = st.secrets["api_key"]
# os.environ["api_key"] == st.secrets["api_key"]
openai.organization = "org-cWYPb9h1vIjpstBy0y6td4Sj"

openai.api_key = os.getenv('api_key')
secret_key = os.getenv('secret_key')

# os.environ[]
# ------------------------------------------------------------------- # 
# defs 
# ------------------------------------------------------------------- #

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

import time

def gpt_proofread(user_input, article):
    retries = 3  # number of retries
    for i in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                temperature = 0,
                max_tokens = 2500,
                messages=[
                    {
                        "role": "system",
                        "content": "As a proficient proofreader with expertise in both English and Korean, your task involves fact-checking two specific texts. The first document is a news article, while the second is a Korean summary of the same article. Your responsibility is to diligently examine both texts, ensuring the contents of the Korean summary accurately reflect the details conveyed in the principal English news article.\nOutput should look like this:\n1)\n- 원문\n=> <original sentence in summary>\n- 수정\n=> <corrected sentence of summary>\n- 수정이유\n=> <Reason in one sentence in Korean>\n-참고된 문장\n=> <referral sentences of news article for fact checking>"
                    },
                    {
                        "role": "user",
                        "content": "```[news article]\n{}\n```\n\n```[summary]\n{}\n```".format(article, user_input)
                    }
                ]
            )
            return completion.choices[0].message.content

        except Exception as e:
            if i < retries - 1:  # i is zero indexed
                print(f'Request failed {retries} attempts. Error: {e}')
                time.sleep(5)
                continue
            else:
                print(f'Request failed after {retries} attempts. Error: {e}')
                return None  # or some other value indicating failure

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #


def click_element(selector, type):
    if type == 'css':
        click_button = browser.find_element(by = By.CSS_SELECTOR, value = selector)
    if type == 'xpath':
        click_button = browser.find_element(by = By.XPATH, value = selector)
    try:
        click_button.click()
    except:
        browser.execute_script('arguments[0].click()', click_button)

def format_text(text):
    text = text.replace("☐", "\n\n☐").replace(" - ", "\n- ")
    return text.strip()


def repl(match):
    return '<span class="correction"> [[ ' + match.group(1) + ' ]] </span>'



def proof_read(text):
    try:
        browser.get('http://speller.cs.pusan.ac.kr')
        input_element = browser.find_element(by = By.ID, value = 'text1')
        input_element.send_keys(text)
        click_element( '#btnCheck', 'css')
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'tdCorrection1stBox')))
        html_element = browser.find_element(by = By.ID, value = 'tdCorrection1stBox')
        html = html_element.get_attribute('innerHTML')
        # html = html_element.text
        html = re.sub(r'<span class="correction">(.*?)</span>', repl, html)
        html = html.replace('\n', '<br>')
        # html = format_text(html)
    finally:
        browser.quit()
    
    return html
    

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #


# # Initialize the history in the session state
# if "history" not in st.session_state:
#     st.session_state["history"] = []
# # Create the history tab in the sidebar
# st.sidebar.markdown('# 	:speech_balloon: History')
# st.sidebar.caption(':warning: 페이지를 새로고침하면 히스토리가 사라집니다')
# st.sidebar.markdown('---')


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

#
# Title
#
st.title(":blue[EC21R&C] Proof Reader")
st.divider()
#
#
#

#
# 1. 맞춤법 검사
#

st.header('맞춤법 검사')

placeholder = """[검수 대상 텍스트 입력]"""

with st.form("proofread"):
    user_input = st.text_area("_인터넷 연결이 필요해요_", placeholder = placeholder, height = 500)
    # user_input = user_input.replace('\n\n', ' ').replace('\n', ' ').strip()
    submit = st.form_submit_button("**맞춤법 검사 시작**", use_container_width = True)


if submit and user_input:
    with st.spinner("_고치고 있습니다..._"):
    # create a chrome options object and set the headless argument to True
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        # pass the chrome options object to the webdriver.Chrome() constructor
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(15)
        html = proof_read(user_input)
        st.session_state["proofread_result"] = html
else:
    if submit and len(user_input) == 0:
        st.error('텍스트를 입력하세요', icon="🚨")

if "proofread_result" in st.session_state:
    st.divider()
    st.components.v1.html(st.session_state["proofread_result"], width=None, height=400, scrolling=True)
    st.caption('_부산대 맞춤법 검사기 사용_')
    st.divider()

else:
    st.divider()
    st.components.v1.html(html, width=None, height=400, scrolling=True)
    st.caption('_부산대 맞춤법 검사기 사용_')
    st.divider()
#
#
#
st.divider()
#
#
#



st.header('팩트체크')

placeholder_article = '[참고기사나 문장, 단락 등을 입력]'

with st.form("form_gpt"):
        # secret key
    # secret_key_user = st.text_input(':secret: **Secret Key**', placeholder = 'chan@ec21rnc.com에 문의해주세요')
    secret_key_user = st.text_input(':secret: **Secret Key**', placeholder = 'chan@ec21rnc.com에 문의해주세요')
    user_input_article = st.text_area("_참고한 기사를 입력해주세요_", placeholder = placeholder_article, height = 500)
    submit_summary = st.form_submit_button(":printer: **팩트체크시작** :printer:", use_container_width = True)

st.divider()

if submit_summary and user_input and user_input_article and secret_key == secret_key_user:
    with st.spinner("GPT가 읽어보고 있습니다..."):
        result = gpt_proofread(user_input, user_input_article)
        st.markdown(result)
    st.divider()

elif len(user_input_article) == 0 and submit_summary:
    st.error('참고한 기사를 입력하세요', icon="🚨")
elif len(user_input_article) != 0 and submit_summary and len(secret_key_user) != 0 and secret_key != secret_key_user:
    st.error('올바른 `Secret Key`를 입력하세요', icon="🚨")
elif len(user_input_article) != 0 and submit_summary and len(secret_key_user) == 0:
    st.error('`Secret Key`를 입력하세요', icon="🚨")
else:
    pass
#
#
#
