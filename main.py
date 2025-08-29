response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7,   # 🔥 Updated temperature value
    top_p=0.9,
    max_tokens=500
)
