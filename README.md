# Handwritten Notes Digitization & Search

This project builds a **pipeline** to digitize **handwritten medical notes**,  
store them in a **vector database (FAISS)**, and provide a **searchable Fast API**.

---

## Features
- **OCR Extraction** – Uses **AWS Textract** to extract text from handwritten images or PDFs.
- **Cleaning & Structuring** – Cleans and stores extracted text in JSON.
- **Vector Search** – Embeds text using **Sentence-Transformers** and stores vectors in **FAISS**.
- **FastAPI Search API** – Query notes by keyword and get the most relevant matches.

---

## Project Structure
```
handwritten-notes-digitization/
├─ sample_data/          # Add handwritten images or PDFs here
├─ models/               # Stores extracted.json, metadata.json, faiss.index
├─ textract_extract.py   # Extract text using AWS Textract
├─ embed_and_index.py    # Create embeddings and build FAISS index
├─ app.py                # FastAPI app to query indexed notes
├─ utils.py              # Helper functions
├─ requirements.txt      # Python dependencies
└─ README.md             # Project documentation
```

---

## Prerequisites
- **Python 3.8+**
- **AWS Account** (Free tier is fine)
- AWS Textract enabled in your region.

### Set up AWS Credentials
Create a free AWS account: [https://aws.amazon.com/free](https://aws.amazon.com/free)

Configure AWS CLI (one-time):
```bash
aws configure
```
Enter:
- **AWS Access Key ID**
- **AWS Secret Access Key**
- Default region (e.g., `us-east-1`)
- Output format (`json`)

These credentials allow the Python SDK (`boto3`) to call AWS Textract.

---

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/<your-username>/handwritten-notes-digitization.git
cd handwritten-notes-digitization
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

---

## 🔧 Usage

### Step 1 – Extract Text
Place handwritten images or PDFs in the `sample_data/` folder.

Run the extraction script:
```bash
python textract_extract.py --input sample_data --output models/extracted.json
```
This will call **AWS Textract** and save the extracted text to `models/extracted.json`.

---

### Step 2 – Build Vector Index
Create sentence embeddings and store them in FAISS:
```bash
python embed_and_index.py \
    --extracted models/extracted.json \
    --index models/faiss.index \
    --meta models/metadata.json
```

---

### Step 3 – Start FastAPI Server
Run the API server:
```bash
uvicorn app:app --reload --port 8000
```
API will be available at:
```
http://127.0.0.1:8000/search
```

---

## 🔎 Example API Query
Search for notes containing **chest pain**:
```
GET http://127.0.0.1:8000/search?q=chest pain&k=5
```
Response:
```json
[
  {
    "score": 0.12,
    "file": "sample_data/note1.jpg",
    "text": "Patient complains of chest pain and dizziness..."
  },
  ...
]
```
- `q` – Query text
- `k` – Number of results to return (default = 5)

---

## Technologies Used
| Component        | Technology |
|------------------|-----------|
| OCR Extraction   | AWS Textract |
| Embeddings       | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector Database  | FAISS |
| Backend API      | FastAPI |

---

## Deliverables
- **GitHub Repository** – Source code with all scripts and README.
- **Demo** – Run locally and query the API for keyword-based note retrieval.

---

## Notes
- AWS Textract free tier provides **1,000 pages/month** of free text extraction.
- Make sure AWS credentials are set up correctly (`~/.aws/credentials` or environment variables).
- Use dummy handwritten notes if no real medical data is available.

---
