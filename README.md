# SCDP
Modern hunting and tourism website for SCDP (Североцентралното държавно предприятие).

## Quick Start

```bash
# Complete rebuild
./rebuild_all.sh

# Start local server
cd website && python3 -m http.server 8000
```

## Architecture

### Core Scripts

- **`build_from_json.py`** - Main website builder
  - Generates all HTML pages (hotels, services, news, contacts, hunt-marks)
  - Creates modern UI with modals
  - Integrates hunt marks page from JSON data

- **`crawl_hunt_marks.py`** - Hunt marks data extraction
  - Scrapes hunting records from scdp.bg/booking/hunt-marks
  - Handles legacy offset-based pagination (page=0, 50, 100, 150...)
  - Fetches all pages automatically (typically ~30 pages, 1500+ records)
  - Outputs to `hunt_marks_data.json`
  - Run separately to update hunt marks data

- **`crawl_booking_site.sh`** - Website content crawler
  - Downloads content from scdp.bg/booking
  - Extracts images, files, and page content
  - Outputs to `booking_content.json`

### Data Files

- **`hunt_marks_data.json`** - Hunt marks records (scraped separately)
- **`booking_content.json`** - Main website content

### Build Process

1. Clean old files
2. Download hero images (if needed)
3. Crawl main website content
4. Scrape hunt marks data (or use sample)
5. Build complete website (all pages including hunt marks)

## Development

### Update Hunt Marks Data

```bash
# Scrape real data
python3 crawl_hunt_marks.py

# Or use sample data for testing
python3 create_sample_hunt_marks.py
```

### Rebuild Website

```bash
# Full rebuild
./rebuild_all.sh

# Or just rebuild pages (keep data)
python3 build_from_json.py
```

## Features

- ✨ Modern responsive design
- 🖼️ Modal-based details view
- 📱 Mobile-friendly navigation
- 🦌 Filterable hunt marks table
- 📄 Paginated data display (top & bottom)
- 🔍 Search across all fields
- 🎨 Clean, professional UI

## File Structure

```
scdp.github.io/
├── build_from_json.py        # Main website builder (all pages)
├── crawl_hunt_marks.py        # Hunt marks data scraper
├── crawl_booking_site.sh      # Website content crawler
├── create_sample_hunt_marks.py # Sample data generator
├── download_hunting_images.sh # Hero images downloader
├── rebuild_all.sh             # Complete rebuild script
├── hunt_marks_data.json       # Hunt marks data
├── booking_content.json       # Website content
├── hunting_hero_images/       # Hero background images
└── website/                   # Generated website
    ├── index.html
    ├── hotels.html
    ├── services.html
    ├── news.html
    ├── contacts.html
    ├── hunt-marks.html
    ├── assets/
    │   ├── css/
    │   └── js/
    └── images/
```

## Notes

- Hunt marks page is generated as part of the main build process
- Data extraction scripts (`crawl_*.py`) are separate and run independently
- All HTML generation happens in `build_from_json.py`
- No documentation overhead - clean and simple architecture

