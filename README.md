# Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dm3tr0/bmw-scraper.git
   cd bmw-scraper
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Mac
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   # or
   pip install scrapy scrapy-playwright
   ```

4. **Install Playwright Browsers**
   Playwright requires specific browser binaries to run. Install the Chromium browser by running:
   ```bash
   playwright install chromium
   ```

## Running the Spider

To execute the scraper and begin populating the database, run the following command from the root directory of the project:

```bash
scrapy crawl bmw_spider
```
