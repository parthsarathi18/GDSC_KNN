from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GENAI_API_KEY'))  # Assuming you have an API key for GenAI

model = genai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert in understanding invoices."},
        {"role": "user", "content": "we will upload an image as an invoice, and you will have to answer any questions based on the uploaded invoice image."},
    ]
)

def get_gemini_response(input, image_data, user_prompt):
    input_message = {"role": "user", "content": input}
    image_message = {"role": "user", "content": image_data}
    prompt_message = {"role": "user", "content": user_prompt}
    
    model['messages'].extend([input_message, image_message, prompt_message])
    response = genai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=model['messages']
    )
    
    return response['choices'][0]['message']['content']

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [{
            'mine_type': uploaded_file.type,
            'data': bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')

st.header('Multilanguage Invoice extractor')

input_prompt = st.text_input('Input Prompt', key='input')
uploaded_file = st.file_uploader('Image', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded File', use_column_width=True)

sub = st.button("Tell me about the invoice")

if sub:
    with st.spinner("Wait"):
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_prompt)
        st.subheader("The response is")
        st.text_area(label="", value=response, height=500)
