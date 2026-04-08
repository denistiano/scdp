#!/bin/bash

# Complete rebuild script - does everything in the right order
# Usage: ./rebuild_all.sh

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}   SCDP Website Complete Rebuild${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# Step 1: Clean everything
echo -e "${YELLOW}[1/5] Cleaning old files...${NC}"
rm -rf website booking_content.json booking_images booking_files
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# Step 2: Download hunting hero images
echo -e "${YELLOW}[2/5] Downloading hunting hero images...${NC}"
if [ ! -d "hunting_hero_images" ] || [ -z "$(ls -A hunting_hero_images 2>/dev/null)" ]; then
    ./download_hunting_images.sh
else
    echo -e "${GREEN}✓ Hero images already exist${NC}"
fi
echo ""

# Step 3: Crawl the website (includes logo download)
echo -e "${YELLOW}[3/5] Crawling scdp.bg/booking...${NC}"
./crawl_booking_site.sh
echo ""

# Step 4: Scrape hunt marks data
echo -e "${YELLOW}[4/5] Scraping hunt marks data...${NC}"
if python3 crawl_hunt_marks.py; then
    echo -e "${GREEN}✓ Hunt marks data scraped${NC}"
else
    echo -e "${YELLOW}⚠ Hunt marks scraping failed, using sample data${NC}"
    python3 create_sample_hunt_marks.py
fi
echo ""

# Step 5: Build the complete website (includes hunt marks)
echo -e "${YELLOW}[5/5] Building complete website...${NC}"
python3 build_from_json.py
echo ""

echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ Complete rebuild finished!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Website built with:"
echo "  • Main pages (hotels, services, news, contacts)"
echo "  • Hunt marks page (справка отстрел)"
echo "  • Responsive design"
echo "  • Modern UI with modals"
echo ""
echo "To start the server:"
echo "  cd website && python3 -m http.server 8000"
echo ""



