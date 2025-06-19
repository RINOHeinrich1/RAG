from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

model_name = "google/flan-t5-base" #"google-t5/t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = 0 if torch.cuda.is_available() else -1
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=device)

def generate(text,temperature=0.5):
    outputs = generator(text, max_new_tokens=150, do_sample=True, temperature=temperature)
    return outputs[0]["generated_text"].strip()
