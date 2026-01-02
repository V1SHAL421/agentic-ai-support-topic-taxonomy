import json
import os
from pydantic import ValidationError
from llama_cpp import Llama
from app.schemas.taxonomy_data import TaxonomyOutput

llm = Llama(
    model_path="models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=4,
    verbose=False
)

def infer(model: str, system_prompt: str, user_prompt: str, max_tokens: int = 150, temp: float = 0.1):
    prompt = f"{system_prompt}{user_prompt}\nJSON:"
    
    response = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temp,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        stream=False
    )
    
    content = response['choices'][0]['text'].strip()
    print(f"Raw output: {content}")
    return validate_output(json.loads(content))

def validate_output(output: dict):
    try:
        return TaxonomyOutput.model_validate(output)
    except ValidationError as e:
        raise ValueError(f"Invalid taxonomy output: {e}")