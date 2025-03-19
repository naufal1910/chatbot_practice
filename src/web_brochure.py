#import
import os
import requests
import gradio as gr
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import display, Markdown, update_display
from openai import OpenAI

#load env
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print("OpenAI API key loaded successfully.")
else:
    print("OpenAI API key not found in environment variables.")

MODEL = 'gpt-4o-mini'
openai = OpenAI()

#initialize
##class for webpage
class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\n\nWebpage Contents:\n{self.text}\n\n"

##system variables
system_message = "You are an assistant that analyzes the contents of a company website landing page \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown."

##function
###stream brochure
def stream_brochure(company_name, url):
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += Website(url).get_contents()
    completion = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}],
            stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)

    for chunk in completion:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```","").replace("markdown","")
        update_display(Markdown(response), display_id=display_handle.display_id)
        yield response

#process
##testing
stream_brochure("HUGGINGFACE", "https://huggingface.co/")

##implement gradio interface
view = gr.Interface(
    fn=stream_brochure,
    inputs=[gr.Textbox(label="Company name:"), gr.Textbox(label="URL:")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)
view.launch()

