import sys
import io

from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
import torch


# Force UTF-8 output to work correctly with Windows and C#
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

model_name = "dumitrescustefan/bert-base-romanian-cased-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)
correcter = pipeline("fill-mask", model=model, tokenizer=tokenizer)


def restore_diacritics(text):
    
    words = text.split()
    restored_words = []
    
    for word in words:
        # Skip words that already have diacritics or are short/not alphabetic
        if any(char in "ăâîșțĂÂÎȘȚ" for char in word) or not word.isalpha():
            restored_words.append(word)
            continue
        
        # Mask the word and predict corrections
        masked_text = f"{' '.join(words[:words.index(word)])} [MASK] {' '.join(words[words.index(word)+1:])}"
        predictions = correcter(masked_text)
        
        # Select the best prediction (top candidate)
        best_prediction = predictions[0]["token_str"]
        restored_words.append(best_prediction)
    
    restored_text = " ".join(restored_words)
    return restored_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python python_script.py <text>")
        sys.exit(1)

    input_text = sys.argv[1]
    restored_text = restore_diacritics(input_text)
    print(restored_text)