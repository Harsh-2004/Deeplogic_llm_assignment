# Document Processing Chatbot README

## Overview

This project is a Streamlit-based web application that processes PDF documents. It extracts text and images, performs OCR on the images, and utilizes AI models for various NLP tasks such as text cleaning, entity extraction, relationship extraction, summarization, document classification, and answering questions about the document. The chatbot interface allows users to interact with the document in a conversational manner.

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- Tesseract OCR
- Streamlit
- Required Python packages (listed below)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/document-processing-chatbot.git
   cd document-processing-chatbot
   ```

2. **Install required Python packages:**
   ```bash
   pip install openai streamlit streamlit-chat pymupdf pytesseract pillow nltk cohere
   ```

3. **Download Tesseract OCR:**
   - Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
   - Note the installation path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`).

4. **Download NLTK data:**
   ```python
   import nltk
   nltk.download('punkt')
   ```

### Configuration

1. **Set up API keys:**
   - Replace the placeholders with your actual API keys in the script:
     ```python
     openai_client = OpenAI(api_key='your-openai-api-key')
     co = cohere.Client('your-cohere-api-key')
     ```

2. **Tesseract configuration:**
   - Set the path to the Tesseract executable:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

## Running the Application

Run the application using Streamlit:
```bash
streamlit run app.py
```

## Features

### 1. Document Upload
- Users can upload a PDF document through the Streamlit interface.

### 2. Text and Image Extraction
- Extracts text from the PDF.
- Extracts images and performs OCR on them using Tesseract.

### 3. Text Cleaning
- Cleans the extracted text by removing extra whitespace and special characters.

### 4. NLP Tasks
- **Entity Extraction:** Uses Cohere's model to extract entities from the text.
- **Relationship Extraction:** (Placeholder for relationship extraction logic).
- **Text Summarization:** Summarizes the document text using Cohere's model.
- **Document Classification:** Classifies the document text using predefined examples and Cohere's model.

### 5. Chatbot Interface
- Allows users to ask questions about the document.
- Generates responses using OpenAI's GPT model.

## Code Structure

```plaintext
document-processing-chatbot/
│
├── app.py                 # Main application script
├── requirements.txt       # List of required Python packages
├── README.md              # Project documentation
├── output.txt             # File for storing raw extracted text
└── output_1.txt           # File for storing cleaned and tokenized text
```

## Functions

### `clean_text(text)`
Cleans the extracted text by removing extra whitespace and special characters.

### `get_embeddings(text)`
Gets embeddings for the text using Cohere's embedding model.

### `extract_entities(text)`
Extracts entities from the text using Cohere's entity extraction model.

### `extract_relationships(entities)`
Extracts relationships between entities (currently a placeholder).

### `summarize_text(text)`
Summarizes the document text using Cohere's summarization model.

### `classify_document(text)`
Classifies the document text as spam or not spam using Cohere's classification model.

### `generate_response(prompt)`
Generates a response to a user query using OpenAI's GPT model.

## Usage

1. **Upload a PDF document** through the Streamlit interface.
2. The application processes the document, extracts text and images, and performs OCR on images.
3. The cleaned text is displayed, along with tokenized sentences and words.
4. The document is classified, summarized, and users can interact with the document using the chatbot interface.

## Notes

- Ensure that the Tesseract OCR path is correctly configured.
- Replace the API keys with your actual keys.
- The relationship extraction function is a placeholder and needs to be implemented.

## Acknowledgements

- [OpenAI](https://www.openai.com)
- [Cohere](https://cohere.ai)
- [Streamlit](https://streamlit.io)
- [PyMuPDF](https://pymupdf.readthedocs.io)
- [Pytesseract](https://github.com/madmaze/pytesseract)
- [NLTK](https://www.nltk.org)
