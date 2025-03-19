#imports
import os
import requests
import gradio as gr
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

#load env
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print("OpenAI API key loaded successfully.")
else:
    print("OpenAI API key not found in environment variables.")

#connect model
openai = OpenAI()

#initialize message 1
system_message = "You are a helpful assistant"

def message_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return completion.choices[0].message.content

#execute model with message
message_gpt("What is today's date?")

#setup interface
##test before use interface
def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

shout("Hello, World!")

##call interface
gr.Interface(fn=shout, inputs="textbox", outputs="textbox").launch()

##call interface in public
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)

##call interface with browser automatically
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)

#implement function
view = gr.Interface(
    fn=message_gpt,
    inputs = [gr.Textbox(label="Enter your prompt here : ", lines=6)],
    outputs = [gr.Textbox(label="Output : ", lines=8)],
    flagging_mode = "never"
)
view.launch()

#implement markdown
system_message = "You are a helpful assistant that responds in markdown"
view = gr.Interface(
    fn=message_gpt,
    inputs = [gr.Textbox(label="Your Message: ")],
    outputs = [gr.Markdown(label="Response : ")],
    flagging_mode = "never"
)
view.launch()

##setup function for stream
def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

#call function for stream
view = gr.Interface(
    fn=stream_gpt,
    inputs = [gr.Textbox(label="Enter your prompt here : ")],
    outputs = [gr.Markdown(label="Output : ")],
    flagging_mode="never"
)
view.launch()