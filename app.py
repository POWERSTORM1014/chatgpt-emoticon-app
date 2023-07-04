import streamlit as st
import openai

st.title("엠파스봇의 이모티콘 생성기")
openai.api_key = st.secrets["apikey"]
with st.form("form"):
    user_input = st.text_input("만들고 싶은 이모티콘의 표정이나 행동을 적어주세요.")
    image_size = st.selectbox(
        "이모티콘 크기를 선택하세요", ("1024x1024", "512x512", "256x256"))
    submit = st.form_submit_button("만들기")

    if submit and user_input:
        gpt_prompt = [
            {
                "role": "system",
                "content": "You are an artistic AI with the unique ability to create emoticons based on provided descriptions of emotions or actions. Your goal is to accurately represent these emotions or actions in a fun and engaging emoticon style.",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]

        with st.spinner("이모티콘 생성 중..."):
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=gpt_prompt
            )

        image_prompt = gpt_response["choices"][0]["message"]["content"]

        # Translate English image prompt to Korean
        translation_prompt = [
            {
                "role": "system",
                "content": "You are a highly skilled translator capable of translating English to Korean. Please translate the following text.",
            },
            {
                "role": "user",
                "content": image_prompt,
            },
        ]

        with st.spinner("번역 중..."):
            translation_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=translation_prompt
            )

        image_prompt_korean = translation_response["choices"][0]["message"]["content"]

        st.write(image_prompt_korean)
        with st.spinner("그림 그리는중..."):
            dalle_response = openai.Image.create(
                prompt=image_prompt, size=image_size)

        st.image(dalle_response["data"][0]["url"])
