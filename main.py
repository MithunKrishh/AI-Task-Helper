# main.py
from openai import OpenAI

def zero_shot_demo():
    print("\n--- Zero Shot Prompting Demo ---")

    prompt = "Translate the following English sentence into French: 'How are you today?'"
    print(f"Prompt: {prompt}")

    # Initialize client (make sure OPENAI_API_KEY is set in env)
    client = OpenAI()

    # Actual API call with top_p
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7,
        top_p=0.9   # ✅ added top_p
    )

    # Extract text response
    output = response.choices[0].message.content
    print(f"AI Response: {output}")


if __name__ == "__main__":
    zero_shot_demo()
