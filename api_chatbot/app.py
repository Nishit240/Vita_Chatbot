import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn


# import pandas as pd
# df = pd.read_csv("qa_data.csv")
# questions = df["question"].tolist()
# answers = df["answer"].tolist()


# Load dataset
with open("qa_data.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

questions = [item["question"] for item in qa_data]
answers = [item["answer"] for item in qa_data]


# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# FastAPI app
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    user_q = query.question
    user_vec = vectorizer.transform([user_q])
    similarity = cosine_similarity(user_vec, X)
    best_match_idx = similarity.argmax()
    best_answer = answers[best_match_idx]
    confidence = similarity[0][best_match_idx]

    # Replace newline characters with <br> for HTML display
    best_answer_html = best_answer.replace("\n", "<br>")

    return {"answer": best_answer_html, "confidence": float(confidence)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
