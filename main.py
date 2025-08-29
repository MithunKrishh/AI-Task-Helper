# main.py

from openai import OpenAI

client = OpenAI()

# --- System Prompt (RTFC framework) ---
system_prompt = """
Role:
You are an AI task assistant that helps users break down and solve coding, Git, and API-related tasks step by step.

Task:
Provide clear, structured, and beginner-friendly guidance for each request. Always include explanations with reasoning, commands, and example code if needed.

Format:
- Use numbered steps for instructions.
- Provide code blocks for commands/code.
- Keep the tone supportive and professional.

Context:
The AI Task Helper project integrates with OpenAI’s API to guide users through tasks like Git workflow, prompt engineering, code changes, and pull requests.
"""

# --- User Prompt (RTFC framework) ---
user_prompt = """
Role:
I am a developer working on the AI Task Helper project.

Task:
Help me update the AI call parameters (like temperature, top_p, or top_k) and guide me through the Git process to commit changes and create a pull request.

Format:
- Provide code snippets in Python for updating AI call parameters.
- Provide Git commands step by step.
- End with clear instructions to open a PR on GitHub.

Context:
The project is built in Python (main.py) and uses GitHub PR workflow. I am currently updating model parameters and practicing structured prompts.
"""

# --- OpenAI Chat Completion Call ---
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7,  # controls randomness
    top_p=0.9,        # nucleus sampling
    top_k=50,         # limits candidate tokens
    max_tokens=300
)

# --- Print Output ---
print(response.choices[0].message["content"])
