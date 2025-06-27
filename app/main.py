from fastapi import FastAPI, Query
from app.qlik_client import get_qlik_data
from app.gemini_llm import ask_gemini

app = FastAPI(
    title="Qlik + Gemini API Gateway",
    description="Backend for hybrid Qlik Streamlit app",
    version="1.0"
)

# 🚀 Endpoint: Natural Language Q&A with Gemini + Qlik data
@app.get("/ask")
def ask(question: str = Query(..., description="Ask a question about Qlik data")):
    try:
        # 🔄 Fetch structured data from Qlik Engine API
        qlik_data = get_qlik_data()

        # 🧠 Ask Gemini to answer based on that data
        answer = ask_gemini(qlik_data, question)

        return {
            "question": question,
            "answer": answer,
            "data": qlik_data
        }
    except Exception as e:
        return {"error": str(e)}
