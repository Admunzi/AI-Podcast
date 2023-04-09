import openai
import credentials

openai.api_key = credentials.API_KEY


def generate_podcast(content, messages):
    # Add the user message to the messages
    messages.append({"role": "user", "content": content})

    # Generate the response from the assistant
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # Get the response from the assistant
    response_content = response.choices[0].message.content

    # Add the response to the messages
    messages.append({"role": "assistant", "content": response_content})

    return response_content, messages
