import streamlit as st
import json
from agent import run_agent
import os
from PIL import Image
import io
import shutil

# Set page config
st.set_page_config(
    page_title="Text Extraction Agent",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state variables if they don't exist
if 'example' not in st.session_state:
    st.session_state.example = None
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

# Title and description
st.title("📝 Text Extraction Agent")
st.markdown("""
    This application helps you extract and analyze text from images using advanced AI technology.
    Upload an image or select from examples to get started.
""")

# Load examples
def load_examples():
    try:
        with open('examples.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Function to set example
def set_example(example):
    # Copy the example image to a temporary location
    temp_path = f"temp_{os.path.basename(example['img_path'])}"
    shutil.copy2(example['img_path'], temp_path)
    
    # Set session state
    st.session_state.example = example
    st.session_state.current_image = temp_path
    st.session_state.prompt = example['message']

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    # If example is selected or file is uploaded
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Save the uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.current_image = temp_path
        
    # Display example image if selected
    elif 'current_image' in st.session_state and st.session_state.current_image is not None:
        if os.path.exists(st.session_state.current_image):
            image = Image.open(st.session_state.current_image)
            st.image(image, caption="Selected Example Image", use_container_width=True)
    
    # Examples section inside col1
    examples = load_examples()
    
    # Display examples in a vertical list within col1
    for idx, example in enumerate(examples):
        if os.path.exists(example['img_path']):
            # Create a container for each example
            example_container = st.container()
            
            with example_container:
                img = Image.open(example['img_path'])
                
                # Make the image clickable with a button
                if st.button(f"Use Demo", key=f"example_{idx}"):
                    set_example(example)
                st.image(img, use_container_width =True)

with col2:
    st.subheader("Analysis Settings")
    
    # Get prompt from user
    prompt = st.text_area(
        "Enter your prompt",
        value=st.session_state.prompt if 'prompt' in st.session_state and st.session_state.prompt else "",
        placeholder="e.g., Extract key information in bullet points",
        height=132
    )
    
    if st.button("Analyze Image"):
        if 'current_image' not in st.session_state or st.session_state.current_image is None:
            st.error("Please upload an image or select an example first!")
        elif not os.path.exists(st.session_state.current_image):
            st.error("Image file not found. Please upload again.")
        elif not prompt:
            st.error("Please enter a prompt!")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    result = run_agent(st.session_state.current_image, prompt)
                    
                    # Display results in an expandable section
                    with st.expander("View Results", expanded=True):
                        st.markdown("### Extracted Text")
                        st.markdown(result['extracted_text'])
                        
                        st.markdown("### Analysis Result")
                        st.markdown(result['result'][0])
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Cleanup temporary files when the app is done
if 'current_image' in st.session_state and st.session_state.current_image is not None:
    if os.path.exists(st.session_state.current_image):
        try:
            # Only remove if it's a temporary file
            if st.session_state.current_image.startswith("temp_"):
                # Don't remove while the app is running
                pass
        except:
            pass
