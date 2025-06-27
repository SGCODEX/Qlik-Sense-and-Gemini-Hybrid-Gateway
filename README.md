# 📊 Qlik Sense + Gemini Hybrid Gateway in Python

This project builds a powerful **AI-augmented analytics gateway** using:

* **Qlik Engine API** for real-time data extraction
* **Google Gemini LLM** for natural language insights
* **FastAPI** backend for handling data + AI queries
* **Streamlit** frontend for an interactive hybrid dashboard
* **Qlik Capability API (via iframe)** for synced visualizations

---

## 🚀 Project Description

This project is an AI-powered analytics gateway that integrates Qlik Sense dashboards with Google Gemini for natural language querying. It allows users to ask questions about their business data and receive intelligent insights, while also displaying synchronized Qlik visualizations in a unified interface. The entire system is built using Python, combining FastAPI for the backend, Streamlit for the frontend, and WebSocket connections to the Qlik Engine API for real-time data retrieval.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SGCODEX/Qlik-Sense-and-Gemini-Hybrid-Gateway.git
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key

Edit in `app/gemini_llm.py`:

```python
GEMINI_API_KEY = "your_gemini_api_key_here"
```

---

## ▶️ Run Commands

### 🧠 Start the Backend API (FastAPI)

```bash
uvicorn app.main:app --reload
```

Test it by visiting:

```
http://127.0.0.1:8000/ask?question=Which product had highest sales
```

### 🖥️ Launch the Frontend Dashboard (Streamlit)

```bash
streamlit run app.py
```

---

## 🔄 Qlik App Prerequisite

* Make sure **Qlik Sense Desktop** is running
* The app path must be valid in `qlik_client.py`, example:

```python
QLIK_APP_PATH = "C:/Users/Admin/Documents/Qlik/Sense/Apps/SalesAppFromQVD.qvf"
```

* Ensure Qlik's WebSocket server is accessible at:

  ```
  ws://localhost:4848
  ```

---

## ✨ Features

* ✅ Real-time data fetch from Qlik using WebSocket Engine API
* ✅ Natural language Q\&A with Gemini on Qlik data
* ✅ Embedded synced visualizations from Qlik using iframes
* ✅ Unified frontend with AI + Charts via Streamlit

---

## 🧠 Credits

Built by SGCODEX — combining the power of **Qlik Sense** with **Generative AI**.

---
