import streamlit as st
from streamlit_option_menu import option_menu
from transformers import (AutoModel, AutoTokenizer)
from PIL import Image
import numpy as np
import time

tokenizer = AutoTokenizer.from_pretrained('srimanth-d/GOT_CPU', trust_remote_code=True)
model = AutoModel.from_pretrained('srimanth-d/GOT_CPU', trust_remote_code=True, low_cpu_mem_usage=True, use_safetensors=True, pad_token_id=tokenizer.eos_token_id)
model = model.eval()


# Sidebar menu
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Documents'], 
        icons=['house', 'file-earmark-text-fill'], menu_icon="cast", default_index=0)

# Home page (OCR functionality)
if selected == "Home":
    st.title("Image to Text Converter (OCR)")
    st.subheader("An Online Optical Character Recognition")

    # Function to handle OCR
    def OCR():
        uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            # Save uploaded file
            with open(f"{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"File '{uploaded_file.name}' saved successfully!")

            # Open and display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            try:
                # Send image to the OCR model
                with st.spinner('Processing...'):
                    res = model.chat(tokenizer, uploaded_file.name, ocr_type='ocr')
                return res
            except Exception as e:
                st.error(f"Error in OCR processing: {e}")
                return None

    # Call the OCR function
    result = OCR()
    
    # Display OCR result
    if result:
        st.text_area("OCR Result", result)
    else:
        st.info("Upload an image to extract text.")


# Documents page
if selected == "Documents":
    st.header("Documents Requirement")

# Display selected menu item
selected
