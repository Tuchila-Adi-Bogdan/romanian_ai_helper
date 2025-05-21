import sys
import io

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline as hf_pipeline

# Force UTF-8 output to work correctly with Windows and C#
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Model setup
model_name = "ai-forever/mGPT-1.3B-romanian"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set device (CPU or GPU)
device = 0 if torch.cuda.is_available() else -1

# Load the pipeline correctly
text_generator = hf_pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

def restore_diacritics(text):
    prompt = (
    "Text fără diacritice: Georgescu voteaza cu Calin si il trimite la piata.\n"
    "Text cu diacritice: "
)

    output = text_generator(prompt, max_new_tokens=64, do_sample=False)
    return output[0]["generated_text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python python_script.py <text>")
        sys.exit(1)

    input_text = sys.argv[1]
    restored_text = restore_diacritics(input_text)
    print(restored_text)
