#imports
import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import display, Markdown, update_display

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
system_message = "You are a helpful assistant that responds in Markdown"
user_prompt = "How do I decide if a business problem is suitable for an LLM solution? Please respond in Markdown."

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
  ]

#execute model with message

# GPT-4o-mini
completion = openai.chat.completions.create(
    model='gpt-4o-mini',
    messages=prompts,
    temperature=0.7
)
print(completion.choices[0].message.content)

#stream
stream = openai.chat.completions.create(
    model='gpt-4o-mini',
    messages=prompts,
    temperature=0.7,
    stream=True
)

reply = ""
display_handle = display(Markdown(""), display_id=True)
for chunk in stream:
    reply += chunk.choices[0].delta.content or ''
    reply = reply.replace("```","").replace("markdown","")
    update_display(Markdown(reply), display_id=display_handle.display_id)

