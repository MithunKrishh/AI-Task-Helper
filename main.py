# main.py

from openai import OpenAI
import json

client = OpenAI()

# --- System Prompt (RTFC framework) ---
system_prompt = """
Role:
You are an AI task assistant that helps users break down and solve coding, Git, and API-related tasks step by step.

Task:
Provide clear, structured, and beginner-friendly guidance for each request. 
When needed, call functions with structured JSON.

Format:
- Use numbered steps for instructions.
- Provide code blocks for commands/code.
- Keep the tone supportive and professional.

Context:
The AI Task Helper project integrates with OpenAI’s API to guide users through tasks like Git workflow, prompt engineering, code changes, and pull requests.
"""

# --- Define Functions for Function Calling ---
functions = [
    {
        "name": "get_git_commands",
        "description": "Provides git commands for updating a file and creating a pull request",
        "parameters": {
            "type": "object",
            "properties": {
                "branch_name": {
                    "type": "string",
                    "description": "The branch name for the PR"
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message for the change"
                }
            },
            "required": ["branch_name", "commit_message"]
        }
    }
]

# --- User Prompt ---
user_prompt = """
Help me implement function calling in this AI project. 
Update the AI call with function definitions and demonstrate calling it. 
Also guide me with Git commands to commit changes and create a pull request.
"""

# --- AI Call with Function Calling ---
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    functions=functions,
    function_call="auto",  # auto-selects function if needed
    temperature=0.7,
    top_p=0.9,
    max_tokens=300
)

# --- Handle Function Call ---
message = response.choices[0].message

if message.get("function_call"):
    function_name = message["function_call"]["name"]
    args = json.loads(message["function_call"]["arguments"])

    if function_name == "get_git_commands":
        branch = args["branch_name"]
        commit_msg = args["commit_message"]

        git_steps = f"""
        # Git Workflow
        git checkout -b {branch}
        git add main.py
        git commit -m "{commit_msg}"
        git push origin {branch}
        
        # Then open GitHub and create a Pull Request from {branch} -> main
        """
        print(git_steps)
else:
    print(message["content"])
