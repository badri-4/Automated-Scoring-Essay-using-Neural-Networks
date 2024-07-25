import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Essay(BaseModel):
    full_text: str

app = FastAPI()

# Use environment variable for the file path
save_path = os.getenv('MODEL_PATH', './')

try:
    # Load the tokenizer and model from the saved path
    tokenizer = AutoTokenizer.from_pretrained(save_path)
    model = AutoModelForSequenceClassification.from_pretrained(save_path, trust_remote_code=True)
    model.to('cuda' if torch.cuda.is_available() else 'cpu')
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model and tokenizer: {e}")

@app.post("/predict")
def predict(essay: Essay):
    inputs = tokenizer(essay.full_text, return_tensors="pt", truncation=True, padding=True, max_length=2000)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
    score = int(predictions[0] + 1)
    return {"score": score}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
