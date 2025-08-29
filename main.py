from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

class PromptRequest(BaseModel):
    query: str
    mode: str = "zero-shot"  # default mode: zero-shot
    top_p: float = 0.9
    top_k: int = 5

@app.post("/generate")
async def generate_text(request: PromptRequest):
    # Zero-shot prompting
    if request.mode == "zero-shot":
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": request.query}
        ]

    # Multi-shot prompting
    elif request.mode == "multi-shot":
        examples = """
Example 1:
Q: Explain what photosynthesis is to a 10-year-old.
A: Photosynthesis is like cooking for plants. Plants use sunlight, water, and air to make their own food. The leaves act like little kitchens where this happens.

Example 2:
Q: Explain what gravity is to a 10-year-old.
A: Gravity is like an invisible hand that pulls everything down to the ground. It’s why we don’t float away when we jump and why apples fall from trees.

Example 3:
Q: Explain what the internet is to a 10-year-old.
A: The internet is like a giant library and playground that lives inside computers and phones. It helps people share messages, play games, and find information quickly.
"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": examples + f"\nNow it’s your turn:\nQ: {request.query}\nA:"}
        ]

    # Retrieval-augmented generation (Top-K)
    elif request.mode == "top-k":
        retrieved_docs = [f"Document {i+1}: Content snippet here." for i in range(request.top_k)]
        context = "\n".join(retrieved_docs)
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant using retrieved context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.query}"}
        ]

    else:
        return {"error": "Invalid mode. Use 'zero-shot', 'multi-shot', or 'top-k'."}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        top_p=request.top_p
    )

    return {"response": response.choices[0].message["content"]}
