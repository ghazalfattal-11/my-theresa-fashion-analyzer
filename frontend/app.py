"""
Streamlit Frontend for Fashion Image Analysis
Beautiful, modern UI for analyzing fashion images with AI
"""

import streamlit as st
import requests
from PIL import Image
import io
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Fashion Image Analysis",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .upload-text {
        text-align: center;
        color: #666;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://127.0.0.1:8000"

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/clothes.png", width=80)
    st.title("Fashion AI Analyzer")
    st.markdown("---")
    
    st.markdown("### 📋 Features")
    st.markdown("""
    - 🖼️ Upload fashion images
    - 🤖 AI-powered analysis
    - 👔 Detailed descriptions
    - 🎨 Color & style detection
    - 📊 View scraped images
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    This app uses AWS Bedrock (Claude 3) to analyze fashion images and provide detailed descriptions.
    """)
    
    # API Health Check
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

# Main content
st.title("👔 Fashion Image Analysis")
st.markdown("Upload a fashion image to get detailed AI-powered analysis")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "🖼️ Scraped Images", "📊 Statistics"])

# Tab 1: Upload & Analyze
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a fashion image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of clothing or fashion item"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Image info
            st.markdown("**Image Details:**")
            st.write(f"- Format: {image.format}")
            st.write(f"- Size: {image.size[0]} x {image.size[1]} pixels")
            st.write(f"- Mode: {image.mode}")
    
    with col2:
        st.markdown("### Analysis Results")
        
        if uploaded_file is not None:
            # Analyze button
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing image with AI... This may take a few seconds."):
                    try:
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        # Send to API
                        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        response = requests.post(f"{API_URL}/analyze", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Display success
                            st.success("✅ Analysis Complete!")
                            
                            # Display analysis
                            st.markdown("### 🤖 AI Analysis")
                            st.markdown(result['analysis'])
                            
                            # Display image info
                            with st.expander("📊 Technical Details"):
                                st.json(result['image_info'])
                        
                        else:
                            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Make sure the FastAPI server is running.")
                        st.code("python -m uvicorn app.main:app --reload")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Upload an image to start analysis")

# Tab 2: Scraped Images
with tab2:
    st.markdown("### 🖼️ Browse Scraped Images")
    
    # Category selector
    categories = [
        "men_clothing",
        "women_clothing",
        "gucci_under_1000",
        "elie_saab",
        "men_shoes"
    ]
    
    selected_category = st.selectbox(
        "Select Category",
        categories,
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    # Get images from category
    data_path = Path("scraper/data") / selected_category
    
    if data_path.exists():
        image_files = list(data_path.glob("*.jpg")) + list(data_path.glob("*.jpeg")) + list(data_path.glob("*.png"))
        
        if image_files:
            st.write(f"Found {len(image_files)} images in {selected_category}")
            
            # Number of images to show
            num_images = st.slider("Number of images to display", 1, min(50, len(image_files)), 12)
            
            # Display images in grid
            cols = st.columns(4)
            for idx, img_path in enumerate(image_files[:num_images]):
                with cols[idx % 4]:
                    try:
                        img = Image.open(img_path)
                        st.image(img, caption=img_path.name, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {str(e)}")
        else:
            st.warning(f"No images found in {selected_category}")
            st.info("Run the scraper first: `python scrape_and_save.py`")
    else:
        st.warning(f"Category folder not found: {data_path}")
        st.info("Run the scraper first: `python scrape_and_save.py`")

# Tab 3: Statistics
with tab3:
    st.markdown("### 📊 Scraping Statistics")
    
    # Get statistics
    data_path = Path("scraper/data")
    
    if data_path.exists():
        stats = {}
        total_images = 0
        
        for category in categories:
            cat_path = data_path / category
            if cat_path.exists():
                count = len(list(cat_path.glob("*.jpg")) + list(cat_path.glob("*.jpeg")) + list(cat_path.glob("*.png")))
                stats[category] = count
                total_images += count
            else:
                stats[category] = 0
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Images", total_images)
        with col2:
            st.metric("Men's Clothing", stats.get("men_clothing", 0))
        with col3:
            st.metric("Women's Clothing", stats.get("women_clothing", 0))
        with col4:
            st.metric("Gucci Items", stats.get("gucci_under_1000", 0))
        with col5:
            st.metric("Men's Shoes", stats.get("men_shoes", 0))
        
        # Progress bars
        st.markdown("### 📈 Collection Progress")
        
        targets = {
            "men_clothing": 500,
            "women_clothing": 500,
            "gucci_under_1000": 20,
            "elie_saab": 50,
            "men_shoes": 100
        }
        
        for category, target in targets.items():
            current = stats.get(category, 0)
            progress = min(current / target, 1.0)
            st.write(f"**{category.replace('_', ' ').title()}**: {current}/{target}")
            st.progress(progress)
        
        # Overall progress
        total_target = sum(targets.values())
        overall_progress = min(total_images / total_target, 1.0)
        st.markdown("### 🎯 Overall Progress")
        st.progress(overall_progress)
        st.write(f"{total_images}/{total_target} images ({overall_progress*100:.1f}%)")
        
    else:
        st.warning("No data folder found. Run the scraper first.")
        st.code("python scrape_and_save.py")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit & FastAPI | Powered by AWS Bedrock (Claude 3)</p>
    </div>
""", unsafe_allow_html=True)
