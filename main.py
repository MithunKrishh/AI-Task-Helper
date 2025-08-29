# dynamic_prompt_with_functions_and_git.py

import subprocess
import json
from openai import OpenAI

client = OpenAI()

# --- Dynamic Variables ---
user_name = "Mithun"
task_type = "Git workflow"
file_name = "main.py"
branch_name = "feature-dynamic-prompt"

# --- Dynamic Prompt Construction ---
system_prompt = f"""
Role:
You are a coding assistant helping {user_name} with software development tasks.

Task:
Guide the user in completing a {task_type}.

Format:
- Provide clear steps.
- Use commands with explanations.
- Highlight common mistakes and fixes.

Context:
This is part of an AI helper project that generates real-time {task_type} instructions 
for files like {file_name} and helps create branches like {branch_name}.
"""

user_prompt = f"""
I just updated {file_name}. 
Please push my changes to a new branch {branch_name} and open a pull request.
"""

# --- Define Functions for Function Calling ---
functions = [
    {
        "name": "git_push_branch",
        "description": "Push changes to a new branch in Git and create a pull request",
        "parameters": {
            "type": "object",
            "properties": {
                "branch_name": {"type": "string", "description": "The name of the branch"},
                "file_name": {"type": "string", "description": "The file being pushed"},
            },
            "required": ["branch_name", "file_name"]
        }
    }
]

# --- AI Call with Function Calling ---
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    functions=functions,
    function_call="auto",  # let the AI decide
    temperature=0.7,
    max_tokens=250
)

# --- Handle AI Response ---
message = response.choices[0].message

if message.get("function_call"):
    func_name = message["function_call"]["name"]
    args = json.loads(message["function_call"]["arguments"])

    print(f"🔧 Function Call: {func_name}")
    print(f"📂 With Arguments: {args}")

    # --- Execute Git Commands ---
    if func_name == "git_push_branch":
        branch = args["branch_name"]
        file = args["file_name"]

        try:
            # Stage file
            subprocess.run(["git", "add", file], check=True)
            # Commit changes
            subprocess.run(["git", "commit", "-m", f"Update {file} with dynamic prompting"], check=True)
            # Create new branch
            subprocess.run(["git", "checkout", "-b", branch], check=True)
            # Push branch
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)
            # Create PR (needs GitHub CLI)
            subprocess.run(["gh", "pr", "create", "--fill"], check=True)

            print(f"✅ Successfully pushed {file} to branch {branch} and created a pull request.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
else:
    print(message["content"])
