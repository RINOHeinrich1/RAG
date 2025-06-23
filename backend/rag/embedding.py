from transformers import CamembertTokenizer, AutoModel
import torch

tokenizer = CamembertTokenizer.from_pretrained("dangvantuan/sentence-camembert-large")
model = AutoModel.from_pretrained("dangvantuan/sentence-camembert-large")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def get_embedding(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=False).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.pooler_output
    return embeddings.cpu().numpy()
