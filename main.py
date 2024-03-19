from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
from elevenlabs import generate, play
import replicate
from replicate.client import Client

# Path
dotenv_path = 'C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys\\.env'
load_dotenv(dotenv_path)

# All keys
openai_api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_key = os.getenv("ELEVEN_LABS_API_KEY")
replicate_key = os.getenv("REPLICATE_API_TOKEN")
langchain_key = os.getenv("LANGCHAIN_KEY")

# Create open ai instance.
openai_llm = OpenAI(api_key=openai_api_key
                    , organization='org-DYJXHbCMXBmANo0C18KTFtBk')
                    # , temperature=0.9)
                    # Apparently cant use temperature = 0.9?)

# help(OpenAI)
# help(generate)

# ---------------- General Langchain tutorial
# langchain_llm = ChatOpenAI(model="gpt-3.5-turbo-1106", organization='org-DYJXHbCMXBmANo0C18KTFtBk')
# can i just use the client from openai? Nope.
# responses = langchain_llm.invoke(
#     [
#         HumanMessage(
#             content="Translate this sentence from English to French: I love programming."
#         )
#     ]
# )
# print(responses.content)
# -------------------------------------------------------
# Use PromptTemplate.
# Generate a half non-static prompt.
# v1
# prompt_template = PromptTemplate.from_template(
#     "Tell me a {adjective} joke about {content}."
# )
# prompt = prompt_template.format(adjective="funny", content="chickens")

# langchain_llm = ChatOpenAI(model="gpt-3.5-turbo-1106", organization='org-DYJXHbCMXBmANo0C18KTFtBk')
# responses = langchain_llm.invoke(
#     [
#         HumanMessage(
#             content=prompt
#         )
#     ]
# )
# print(responses.content)
# llm = LLMChain(llm=langchain_llm, prompt=prompt)

# print(llm.run())

# Openai api, Langchain.
# Todo: Answer: Why do we even need langchain here?
def generate_story(text):
    '''Generate a story using langchain and ChatGPT 3.5'''
    # v2
    prompt_template = PromptTemplate.from_template(
        "{text}"
    )
    # prompt = prompt_template.format(adjective="funny", content="chickens")
    prompt = prompt_template.format(text=text)

    langchain_llm = ChatOpenAI(model="gpt-3.5-turbo-1106", organization='org-DYJXHbCMXBmANo0C18KTFtBk')
    responses = langchain_llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )
    return responses.content

# For testing only:
# print(generate_story("Write a 1 sentence summary about Super Bowl 2024."))

# From replicate
def generate_image(story_text):
    '''
    Generate image based on the output story text with Replicate API
    Additional ideas: Text to Video, Text to Speech
    '''
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
        ,input = {"prompt": story_text}
    )
    return output

# testing
# generate_image("cooking")

# From ElevenLabs
def generate_audio(text, voice):
    audio = generate(text=text, voice=voice, api_key=elevenlabs_key
                     ,model="eleven_monolingual_v1"
                    )
    return audio

# For testing only:
# play(generate_audio("Testing 1 2 3", "Matilda"))

# From streamlit
def app():
    st.title("Story Generator")
    with st.form(key='my_form'):
        text = st.text_input(
            "Enter a word/phrase to generate a story."
            ,max_chars=100
            ,type="default"
            ,placeholder="Enter a word/phrase to generate a story."
        )
        options = ["Matilda", "Josh", "Rachel"]
        voice = st.selectbox("Choose a voice", options)

        if st.form_submit_button("Submit"):
            with st.spinner('Generating story...'):
                story_text = generate_story(text)
                audio = generate_audio(story_text[:100], voice)
            st.audio(audio, format='audio/mp3')
            images = generate_image(story_text)
            for i in images:
                st.image(i)
    if not text or not voice:
        st.info("Please enter a valid word or select a valid voice.")
    
# Only run this if its ran as a standalone program.
if __name__ == '__main__':
    app()