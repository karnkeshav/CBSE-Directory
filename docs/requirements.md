# Project Requirements: CBSE School Scraper & Enrichment System

## Role & Objective
Design and implement a complete scraper pipeline to collect all CBSE-affiliated school details in and around Hyderabad, India, including email addresses, in a safe, scalable, and maintainable way.

The data source is the public CBSE SARAS portal operated by the Central Board of Secondary Education (CBSE).
There is NO official CBSE API. The solution must work via web automation + enrichment.

## 1. Functional Requirements

### Primary Scraper
- Use **Playwright (Node.js)** for scraping (JavaScript is mandatory).
- Target the CBSE SARAS affiliated schools search UI.
- Apply filters:
    - State: **Telangana**
    - Districts:
        - **Hyderabad**
        - **Rangareddy**
        - **Medchal–Malkajgiri**
        - (Optional) Sangareddy
- Handle:
    - Dynamic JavaScript rendering
    - Pagination
    - Intermittent loading delays
- Fields to Extract (per school):
    - CBSE Affiliation Number (primary key)
    - School Name
    - Full Address
    - City
    - District
    - State
    - Pincode
    - Phone Number
    - Email Address (if available)
    - Website URL
    - Source = "saras"
    - Timestamp (last_scraped_at)

## 2. Data Storage
- Use **PostgreSQL** (or Supabase-compatible schema).
- Enforce unique constraint on affiliation number.
- Persist raw scrape data first before enrichment.
- Schema must be explicitly defined.

## 3. Email Enrichment Layer
Implement a 3-pass enrichment pipeline for schools missing email:

### Pass 1 — SARAS Data
- Accept if email is directly present.

### Pass 2 — School Website Scraping
- Fetch homepage and /contact pages.
- Extract emails via:
    - `mailto:` links
    - Regex patterns:
        - `info@`
        - `office@`
        - `admissions@`
        - domain-based school emails

### Pass 3 — Google Maps API (Fallback)
- Search using: "School Name + City"
- Extract:
    - Website
    - Email (if listed)

## 4. Email Validation
- Regex format validation
- MX record existence check
- No email sending or SMTP probing
- Assign confidence level:
    - HIGH → SARAS
    - MEDIUM → Website
    - LOW → Google Maps

## 5. Rate Limiting & Safety Constraints
- Max 1 request per second
- Randomized delays (1.5–3 seconds)
- Retry logic with exponential backoff
- Detect CAPTCHA or blocking and halt safely
- Read-only scraping (no form submission abuse)

## 6. Output & Export
- Export clean data to:
    - CSV
    - Excel (XLSX)
- Provide CLI commands:
    - `scrape`
    - `enrich`
    - `export`

## 7. Project Structure
Generate a clean, professional repository layout, including:
- `scraper/`
- `enrichment/`
- `db/`
- `utils/`
- `config/`
- `README.md`

## 8. Code Quality Expectations
- Modular, readable, well-commented code
- Environment-based config (no hard-coded secrets)
- Clear separation between scraping, enrichment, and export
- Production-safe defaults

## 9. Non-Goals (Do NOT Implement)
- No login bypass
- No CAPTCHA breaking
- No aggressive crawling
- No email sending
- No UI dashboard

## 10. Deliverables
- Full Node.js + Playwright codebase
- PostgreSQL schema
- CLI scripts
- Sample CSV output
- Documentation
