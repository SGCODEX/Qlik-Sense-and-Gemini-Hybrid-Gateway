import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "your_gemini_api_key_here"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(data, question):
    # Prepare the table with all relevant fields
    table = "\n".join([
        f"Product: {row['Product']}, Region: {row['Region']}, Month: {row['Month']}, "
        f"Sales: {row['Sales']}, Units Sold: {row['Units Sold']}"
        for row in data
    ])

    prompt = f"""
You are a smart and analytical assistant. Here's a sales dataset containing the following fields:
Product, Region, Month, Sales, and Units Sold.

Data:
{table}

Question: {question}
Answer concisely in 2–3 lines based on the data.
If needed, compare values and summarize insights directly from the dataset.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
