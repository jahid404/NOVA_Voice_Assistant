import os
import openai

os.environ["OPEN_AI_API"] = "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"
openai.organization = "org-0cAwwpLXyuaKcOBiUk91p25c"
openai.api_key = os.getenv("OPEN_AI_API")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "What is the capital bangladesh?"
        }
    ]
)

print(response['choices'][0]['message']['content']) 
# response = openai.Model.list()
# print(response)