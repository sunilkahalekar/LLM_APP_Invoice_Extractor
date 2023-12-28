# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

# To load all environment variable from .env file
load_dotenv()

import streamlit as st
import os
import pathlib
from PIL import Image
import textwrap

import google.generativeai as genai 

# configure api key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))




## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

# input: whaterver input i have. This input basically is what is assistant to do. In this case it act as invoice extractor.
# This prompt means 

def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# initilize  streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor Demo")

st.header("Multilanguage Application")
input=st.txt_input("Input Prompt:",key="input")
uploaded_file=st.file_uploder("Choose an image of the invoice: ", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)
submit=st.button("Tell me about the invoice")

input_prompt="""
You are expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoce image.
"""

# If submit button is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)
