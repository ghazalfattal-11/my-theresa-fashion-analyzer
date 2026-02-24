# Scraper Module - Modular Architecture

## Structure

```
scraper/
├── config.py                # Configuration and constants
├── selenium_driver.py       # WebDriver setup and management
├── page_scroller.py         # Smart scrolling and content loading
├── product_extractor.py     # Data extraction from elements
├── mytheresa_scraper.py     # Main orchestrator
├── image_fetcher.py         # Fetch images to memory
├── batch_analyzer.py        # Batch analysis with Bedrock
└── results/                 # Analysis results (JSON)
```

## Component Responsibilities

### selenium_driver.py (SeleniumDriver)
**Purpose:** Manage WebDriver lifecycle
- Setup Chrome with optimal options
- Configure headless mode
- Handle driver cleanup
- Prevent detection as bot

### page_scroller.py (PageScroller)
**Purpose:** Handle page scrolling and content loading
- Smart scrolling until target reached
- Detect page bottom
- Click "Load More" buttons
- Scroll elements into view (lazy loading)

### product_extractor.py (ProductExtractor)
**Purpose:** Extract data from HTML elements
- Extract image URLs (multiple attributes)
- Extract brand names
- Extract prices
- Filter invalid data

### mytheresa_scraper.py (MytheresaScraper)
**Purpose:** Orchestrate all components
- Coordinate scraping workflow
- Apply filters (brand, price)
- Manage component lifecycle
- Provide convenience methods

### image_fetcher.py (ImageFetcher)
**Purpose:** Fetch images to memory
- Download images temporarily
- No disk storage
- Error handling



## Data Flow

```
1. MytheresaScraper
   ↓
2. SeleniumDriver (setup browser)
   ↓
3. Load page
   ↓
4. PageScroller (scroll & load content)
   ↓
5. ProductExtractor (extract data)
   ↓
6. Return URLs + metadata
   ↓
7. ImageFetcher (fetch to memory)
   ↓
9. Save results (JSON only)
```

## Benefits

1. **Separation of Concerns**: Each class has one job
2. **Testability**: Easy to test each component
3. **Maintainability**: Changes isolated to specific files
4. **Reusability**: Components can be used independently
5. **Readability**: Smaller, focused files
6. **Extensibility**: Easy to add new features

## Usage Example

```python
from scraper.mytheresa_scraper import MytheresaScraper

# Create scraper (automatically initializes components)
scraper = MytheresaScraper(headless=True)

# Scrape with filters
results = scraper.scrape_category(
    category="men_clothing",
    limit=100,
    brand_filter="Gucci",
    max_price=1000
)

# Or use convenience methods
results = scraper.scrape_gucci_under_1000(limit=20)
```

## Component Interaction

```
MytheresaScraper
    ├── SeleniumDriver
    │   └── Chrome WebDriver
    ├── PageScroller
    │   └── Scrolling logic
    └── ProductExtractor
        └── Data extraction
```

## Design Patterns

1. **Single Responsibility**: Each class does one thing
2. **Dependency Injection**: Components passed to classes
3. **Facade Pattern**: MytheresaScraper provides simple interface
4. **Strategy Pattern**: Different extractors can be swapped

## Testing Individual Components

```python
# Test driver
from scraper.selenium_driver import SeleniumDriver
driver_manager = SeleniumDriver(headless=False)
driver = driver_manager.setup()

# Test scroller
from scraper.page_scroller import PageScroller
scroller = PageScroller(driver)
items = scroller.scroll_and_load(target_items=50)

# Test extractor
from scraper.product_extractor import ProductExtractor
extractor = ProductExtractor(scroller)
data = extractor.extract_from_element(element)
```

## Configuration

All settings in `config.py`:
- URLs and categories
- Scroll timing
- Timeouts
- Price limits
- Browser settings

## Error Handling

Each component handles its own errors:
- Driver: Setup failures
- Scroller: Timeout, stuck pages
- Extractor: Missing elements
- Scraper: Orchestration errors

## Logging

Comprehensive logging at each level:
```
INFO: Component initialization
INFO: Progress updates
DEBUG: Detailed operations
ERROR: Failures with context
```

## Future Extensions

Easy to add:
- Different browsers (Firefox, Edge)
- Parallel scraping
- Proxy support
- Different websites
- Custom extractors
- Caching mechanisms
