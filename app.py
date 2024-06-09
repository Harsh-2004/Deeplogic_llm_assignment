# Imports
import openai
import streamlit as st
from streamlit_chat import message
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import cohere
from cohere import ClassifyExample
from openai import OpenAI

# Define API keys (use your actual API keys)
openai_client = OpenAI(api_key='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')
co = cohere.Client('eGsG0TZYRCtVh5gdsn0Gxx4yHxUgkzJgrGpvrQg5')

nltk.download('punkt')

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()

def get_embeddings(text):
    response = co.embed(model='large', texts=[text])
    return response.embeddings

def extract_entities(text):
    response = co.extract_entities(model='large', text=text)
    return response.entities

def extract_relationships(entities):
    # Implement relationship extraction logic here
    relationships = []
    # Example: Identify relationships based on co-occurrence in sentences
    return relationships

def summarize_text(text):
    response = co.summarize(text=text)
    return response.summary

def classify_document(text):
    examples = [
        ClassifyExample(text="Dermatologists don't like her!", label="Spam"),
        ClassifyExample(text="'Hello, open to this?'", label="Spam"),
        ClassifyExample(text="I need help please wire me $1000 right now", label="Spam"),
        ClassifyExample(text="Nice to know you ;)", label="Spam"),
        ClassifyExample(text="Please help me?", label="Spam"),
        ClassifyExample(text="Your parcel will be delivered today", label="Not spam"),
        ClassifyExample(text="Review changes to our Terms and Conditions", label="Not spam"),
        ClassifyExample(text="Weekly sync notes", label="Not spam"),
        ClassifyExample(text="'Re: Follow up from today's meeting'", label="Not spam"),
        ClassifyExample(text="Pre-read for tomorrow", label="Not spam"),
    ]
    response = co.classify(inputs=[text], examples=examples)
    return response.classifications

# Define chatbot responses using OpenAI
def generate_response(prompt):
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    message = completion.choices[0].message['content'].strip()
    return message

st.title("Document Processing Chatbot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Upload document
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file:
    document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ''
    for page in document:
        page_text = page.get_text()
        text += page_text + "\n"
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)
            text += f"\n[Image {img_index + 1} OCR Text]\n{ocr_text}\n"

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    cleaned_text = clean_text(text)
    sentences = sent_tokenize(cleaned_text)
    tokens = [word_tokenize(sentence) for sentence in sentences]

    with open('output_1.txt', 'w', encoding='utf-8') as f:
        for sentence in tokens:
            f.write(' '.join(sentence) + '\n')

    st.write("Document processed successfully.")

    # Display the text
    with open('output_1.txt', 'r', encoding='utf-8') as f:
        document_text = f.read()

    st.subheader("Document Text")
    st.write(document_text)

    # Classify the document
    classification_results = classify_document(document_text)

    st.subheader("Classification Result")
    for classification_item in classification_results:
        classification_label = classification_item.prediction
        confidence_percentage = round(classification_item.confidence * 100, 2)
        st.write(f"Classification: {classification_label}")
        st.write(f"Confidence: {confidence_percentage}%")

    # Summarize the document
    summary = summarize_text(document_text)
    st.subheader("Summary")
    st.write(summary)

    # Ask questions about the document
    def get_text():
        input_text = st.text_input("You:", "Ask a question about the document", key="input")
        return input_text

    user_input = get_text()
    st.button("Send")

    if user_input:
        prompt = f"Context: {document_text}\n\nQuestion: {user_input}\n\nAnswer:"
        output = generate_response(prompt)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

# Run the app using the following command in the terminal:
# streamlit run app.py
