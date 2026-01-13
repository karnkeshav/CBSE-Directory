# CBSE SARAS Scraper Project

## Setup

1.  Install dependencies:
    ```bash
    npm install
    npx playwright install
    ```

2.  Environment Variables:
    Create a `.env` file with:
    ```
    DATABASE_URL=postgres://user:password@localhost:5432/dbname
    GOOGLE_MAPS_API_KEY=your_key (optional for Pass 3)
    ```

3.  Database Setup:
    Run the schema script to create the table:
    ```bash
    psql -d dbname -f db/schema.sql
    ```

## Usage

### CLI Commands

-   **Scrape SARAS:**
    ```bash
    node scraper/saras_scraper.js
    ```

-   **Enrich Data:**
    ```bash
    node enrichment/enrichment_pipeline.js
    ```

-   **Export Data:**
    ```bash
    node utils/export.js
    ```

## Project Structure

-   `scraper/`: Contains the Playwright scraper script.
-   `enrichment/`: Contains the email enrichment pipeline.
-   `db/`: Database schema and connection logic.
-   `utils/`: Helper functions and export logic.
-   `config/`: Configuration files.
-   `docs/`: Project documentation and requirements.

## Legal & Ethical Usage

-   This scraper is intended for educational and research purposes.
-   Respect the target website's `robots.txt` and terms of service.
-   Do not use the data for spam or unsolicited marketing.
