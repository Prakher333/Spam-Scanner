from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt_tab')
nltk.download("punkt")
nltk.download("stopwords")

ps = PorterStemmer()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Text Preprocessing
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = [word for word in text if word.isalnum()]  # Remove special characters

    y = [word for word in y if word not in stopwords.words('english') and word not in string.punctuation]

    y = [ps.stem(word) for word in y]  # Stemming

    return " ".join(y)

try:
    tfidf = pickle.load(open("models/vectorizer.pkl", "rb"))
    model = pickle.load(open("models/model.pkl", "rb"))
except Exception as e:
    print("Error loading model:", e)
    raise e


class EmailText(BaseModel):
    text: str

@app.post("/predict")
async def predict(email: EmailText):
    if not email.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    # 1. Preprocess input
    transformed_sms = transform_text(email.text)

    # 2. Vectorize input
    vector_input = tfidf.transform([transformed_sms])

    # 3. Predict
    prediction = model.predict(vector_input)[0]
    result = "Not Spam" if prediction == 0  else "Spam"

    return {"prediction": result}
