from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def get_ai_response(prompt: str):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",     # Model selection
        messages=messages,        # Conversation history
        temperature=0.7,          # Controls randomness
        top_p=0.9,                # Nucleus sampling
        top_k=50                  # Limits token selection to top K options
    )

    # Extract the assistant's reply
    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    reply = get_ai_response(user_input)
    print("AI:", reply)
