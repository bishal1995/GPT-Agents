from openai import OpenAI

local_model = "llama3.2:latest"
client=OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="not-needed"
)


# Example function to query ChatGPT
def ask_chatgpt(user_message):
    response = client.chat.completions.create(
        model=local_model,  # gpt-4 turbo or a model of your preference
        messages=[{"role": "system", "content": "You are a dramatic assistant."},
                  {"role": "user", "content": user_message}],
        temperature=0.7,
        )       
    return response.choices[0].message.content


# Example usage
user = "What is your cut off date?"
response = ask_chatgpt(user)
print(response)
