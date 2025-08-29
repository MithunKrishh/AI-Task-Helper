# main.py
def zero_shot_demo():
    print("\n--- Zero Shot Prompting Demo ---")
    prompt = "Translate the following English sentence into French: 'How are you today?'"
    print(f"Prompt: {prompt}")
    
    # Simulated AI response (in a real case, you'd call the LLM API here)
    response = "Comment allez-vous aujourd'hui ?"
    print(f"AI Response: {response}")

if __name__ == "__main__":
    zero_shot_demo()
