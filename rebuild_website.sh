#!/bin/bash

# Rebuild website only - no crawling
# Usage: ./rebuild_website.sh

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}   SCDP Website Rebuild (No Crawling)${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# Check for required files
echo -e "${YELLOW}Checking required files...${NC}"
if [ ! -f "booking_content.json" ]; then
    echo -e "${YELLOW}⚠ Warning: booking_content.json not found${NC}"
    echo "   Run ./crawl_booking_site.sh first to get content"
fi

if [ ! -f "hunt_marks_data.json" ]; then
    echo -e "${YELLOW}⚠ Warning: hunt_marks_data.json not found${NC}"
    echo "   Run python3 crawl_hunt_marks.py to get hunt marks data"
fi

if [ ! -d "hunting_hero_images" ] || [ -z "$(ls -A hunting_hero_images 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠ Warning: Hero images missing${NC}"
    echo "   Run ./download_hunting_images.sh to download them"
fi

echo -e "${GREEN}✓ Checks complete${NC}"
echo ""

# Rebuild website
echo -e "${YELLOW}Building complete website...${NC}"
python3 build_from_json.py

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ Website rebuild finished!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Website location: website/"
echo ""
echo "To start the server:"
echo "  cd website && python3 -m http.server 8000"
echo ""













