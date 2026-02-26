# Fashion Image Analysis - Streamlit Frontend

Beautiful, modern web interface for analyzing fashion images with AI.

## Features

### 📤 Upload & Analyze
- Drag-and-drop image upload
- Real-time image preview
- AI-powered analysis using AWS Bedrock (Claude 3)
- Detailed fashion descriptions
- Color, style, and pattern detection

### 🖼️ Scraped Images Gallery
- Browse all scraped images by category
- View images in a responsive grid
- Quick analyze any scraped image
- Filter by category

### 📊 Statistics Dashboard
- Real-time scraping progress
- Category-wise image counts
- Progress bars for each category
- Overall completion percentage

## Quick Start

### 1. Install Dependencies
```bash
pip install streamlit requests pillow
```

Or install from requirements:
```bash
pip install -r frontend/requirements.txt
```

### 2. Start FastAPI Backend
```bash
# In terminal 1
python -m uvicorn app.main:app --reload
```

### 3. Start Streamlit Frontend
```bash
# In terminal 2
streamlit run frontend/app.py
```

### 4. Open in Browser
The app will automatically open at: `http://localhost:8501`

## Usage

### Upload & Analyze
1. Go to "Upload & Analyze" tab
2. Click "Browse files" or drag-and-drop an image
3. Click "Analyze Image" button
4. View AI-generated analysis

### Browse Scraped Images
1. Go to "Scraped Images" tab
2. Select a category from dropdown
3. Adjust number of images to display
4. Click "Analyze" on any image for instant analysis

### View Statistics
1. Go to "Statistics" tab
2. See total images scraped
3. View progress for each category
4. Track overall completion

## Configuration

### API URL
Default: `http://127.0.0.1:8000`

To change, edit `frontend/app.py`:
```python
API_URL = "http://your-api-url:port"
```

### Port
Default: `8501`

To change:
```bash
streamlit run frontend/app.py --server.port 8502
```

## Features Explained

### Modern UI
- Clean, professional design
- Responsive layout
- Custom CSS styling
- Intuitive navigation

### Real-time API Status
- Sidebar shows API connection status
- Green checkmark when connected
- Red X when offline

### Image Preview
- Instant preview of uploaded images
- Display image dimensions and format
- Show file size and color mode

### AI Analysis
- Detailed fashion descriptions
- Item type identification
- Color and pattern detection
- Style recommendations
- Material suggestions
- Occasion suitability

### Gallery View
- Grid layout for easy browsing
- Lazy loading for performance
- Category filtering
- Quick analyze feature

### Progress Tracking
- Visual progress bars
- Percentage completion
- Category-wise breakdown
- Total image count

## Troubleshooting

### "API Offline" Error
**Solution:** Make sure FastAPI is running:
```bash
python -m uvicorn app.main:app --reload
```

### "No images found" Warning
**Solution:** Run the scraper first:
```bash
python scrape_and_save.py
```

### Port Already in Use
**Solution:** Use a different port:
```bash
streamlit run frontend/app.py --server.port 8502
```

### Images Not Loading
**Solution:** Check that images are in `scraper/data/` folder

## Customization

### Change Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Add New Categories
Edit `categories` list in `frontend/app.py`:
```python
categories = [
    "men_clothing",
    "women_clothing",
    "your_new_category"
]
```

### Modify Layout
Change column ratios:
```python
col1, col2 = st.columns([1, 2])  # 1:2 ratio
```

## Performance

- **Load time:** < 2 seconds
- **Image analysis:** 2-5 seconds (depends on AWS Bedrock)
- **Gallery loading:** Instant (lazy loading)
- **Memory usage:** ~100MB

## Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Tips

1. **Use high-quality images** for best analysis results
2. **Clear, well-lit photos** work better
3. **Single item per image** gives more accurate descriptions
4. **Close-up shots** provide more detail

## Screenshots

### Upload & Analyze
Beautiful interface for uploading and analyzing fashion images.

### Gallery View
Browse all scraped images in an organized grid.

### Statistics
Track your scraping progress with visual metrics.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI:** AWS Bedrock (Claude 3)
- **Image Processing:** Pillow
- **HTTP Client:** Requests

## License

For internship/educational purposes.
