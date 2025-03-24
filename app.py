import streamlit as st
import json
from agent import run_agent
import os
from PIL import Image
import io
import shutil
import time

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
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'results' not in st.session_state:
    st.session_state.results = None

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

# Function to handle demo selection
def handle_demo_selection(example_idx):
    examples = load_examples()
    example = examples[example_idx]
    
    # Copy the example image to a temporary location
    temp_path = f"temp_{os.path.basename(example['img_path'])}"
    shutil.copy2(example['img_path'], temp_path)
    
    # Set session state
    st.session_state.example = example
    st.session_state.current_image = temp_path
    st.session_state.prompt = example['message']
    st.rerun()

# Function to handle analysis
def handle_analysis():
    if 'current_image' not in st.session_state or st.session_state.current_image is None:
        st.error("Please upload an image or select an example first!")
        return
    
    if not os.path.exists(st.session_state.current_image):
        st.error("Image file not found. Please upload again.")
        return
    
    if not st.session_state.prompt:
        st.error("Please enter a prompt!")
        return
    
    # Set processing flag
    st.session_state.processing = True
    st.session_state.results = None
    
    # Force a rerun to show the processing state
    st.rerun()

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
            
            # If processing, add a visual indicator
            if st.session_state.processing:
                st.image(image, caption="Processing image...", use_container_width=True)
                st.markdown("⏳ **Image processing in progress...**")
            else:
                st.image(image, caption="Selected Image", use_container_width=True)
    
    # Examples section inside col1
    examples = load_examples()
    
    # Display examples in a vertical list within col1
    for idx, example in enumerate(examples):
        if os.path.exists(example['img_path']):
            # Create a container for each example
            example_container = st.container()
            
            with example_container:
                if st.button(f"Use Demo {idx + 1}", key=f"example_{idx}"):
                    handle_demo_selection(idx)
                st.markdown(f"**Prompt**: {example['message']}")
                

with col2:
    st.subheader("Analysis Settings")
    
    # Get prompt from user
    prompt = st.text_area(
        "Enter your prompt",
        value=st.session_state.prompt,
        placeholder="e.g., Extract key information in bullet points",
        height=132
    )
    
    # Update prompt in session state
    st.session_state.prompt = prompt
    
    # Analyze button
    if st.button("Analyze Image"):
        handle_analysis()
    
    # If in processing state, show the spinner and process the image
    if st.session_state.processing:
        with st.spinner("Analyzing image..."):
            try:
                # Ensure we have a valid image path before processing
                img_path = st.session_state.current_image
                if img_path and os.path.exists(img_path):
                    # Actual processing
                    result = run_agent(img_path, st.session_state.prompt)
                    
                    # Store results and clear processing flag
                    st.session_state.results = result
                    st.session_state.processing = False
                    
                    # Force a rerun to update the UI
                    st.rerun()
                else:
                    st.error("Invalid image path. Please select an image again.")
                    st.session_state.processing = False
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.processing = False
    
    # Display results if available
    if st.session_state.results is not None:
        with st.expander("View Results", expanded=True):
            st.markdown("### Extracted Text")
            st.markdown(st.session_state.results['extracted_text'])
            
            st.markdown("### Analysis Result")
            st.markdown(st.session_state.results['result'][0])

# Cleanup temporary files when the app is done
if 'current_image' in st.session_state and st.session_state.current_image is not None:
    if os.path.exists(st.session_state.current_image):
        try:
            # Only remove if it's a temporary file
            if os.path.basename(st.session_state.current_image).startswith("temp_"):
                # Don't remove while the app is running
                pass
        except:
            pass
