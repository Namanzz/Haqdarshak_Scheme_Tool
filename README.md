
# 🧠 Haqdarshak Scheme Research Tool

An intelligent, offline tool to automatically summarize government scheme documents and answer questions — powered by LangChain, FAISS, and Hugging Face models.

---

## 📌 Project Objective

At Haqdarshak, the goal is to help citizens access the right government schemes. This project streamlines that mission by:

- Extracting structured summaries from scheme documents (PDFs)
- Enabling users to ask questions in natural language
- Working completely offline — no OpenAI, no API cost

---

## 🎯 Features

- 📝 Paste one or more government scheme PDF URLs
- 📄 Automatically extracts and summarizes:
  - ✅ Scheme Benefits
  - ✅ Eligibility Criteria
  - ✅ Documents Required
  - ✅ Application Process
- 🔍 Ask any question about the content
- ⚡ Fast, lightweight, and free — runs 100% locally
- 📎 Displays source URLs for all answers

---

## 🧰 Tech Stack

| Layer           | Tool/Library                     |
|----------------|----------------------------------|
| UI             | Streamlit                        |
| Embeddings     | sentence-transformers (MiniLM)   |
| Vector Search  | FAISS                            |
| Summarization  | Hugging Face `flan-t5-base`      |
| PDF Parsing    | PyMuPDF (LangChain loader)       |
| QA Engine      | LangChain RetrievalQA            |

---

## 🏗️ Folder Structure

```
Haqdarshak_Scheme_Tool/
├── main.py
├── requirements.txt
├── utils/
│   ├── loader.py
│   ├── qa_engine.py
│   └── summarizer.py
```

---

## ▶️ How to Run

1. **Clone this repo**
   ```bash
   git clone https://github.com/Namanzz/Haqdarshak_Scheme_Tool.git
   cd Haqdarshak_Scheme_Tool
   ```

2. **Create a virtual environment** (optional but recommended)

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run main.py
   ```

---

## 🔗 Sample Scheme PDF URL

Use this to test the app:

```
https://mohua.gov.in/upload/uploadfiles/files/PMSVANidhi%20Guideline_English.pdf
```

---

## ❗ Notes

- Model used: `google/flan-t5-base` (~250MB, auto-downloaded)
- No OpenAI key required
- FAISS index is stored in `faiss_store_openai.pkl` after processing

---

## 📽️ Demo

➡️ https://drive.google.com/file/d/1HRT4qyV7YmeBtjLjnktsBE79OVAlke5N/view?usp=drive_link

---

## 🙋 Author

Made with ❤️ by **Naman Anand**  
For the placement assignment at **Haqdarshak**
