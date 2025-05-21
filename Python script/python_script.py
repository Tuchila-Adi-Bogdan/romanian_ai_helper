import sys
import io

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


# Force UTF-8 output to work correctly with Windows and C#
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

model_name = "ai-forever/mGPT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Use causal LM pipeline instead of text2text
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
    truncation=True,  # ✅ Add this line
)

def restore_diacritics(text):
    prompt = "restore diacritics: " + text
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=128)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    outputs = model.generate(**inputs, max_length=128, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python python_script.py <text>")
        sys.exit(1)

    input_text = sys.argv[1]
    restored_text = restore_diacritics(input_text)
    print(restored_text)