#!/usr/bin/env python3
"""
Hunt Marks Data Scraper for SCDP
Scrapes hunting records from https://scdp.bg/booking/hunt-marks
with support for pagination and filtering
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin, parse_qs, urlparse

# Configuration
BASE_URL = "https://scdp.bg/booking/hunt-marks"
OUTPUT_FILE = "hunt_marks_data.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_page(url, params=None):
    """Fetch a page with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"  Fetching: {url} (params: {params})")
            response = requests.get(url, headers=HEADERS, params=params, timeout=15)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return None
    return None

def extract_filters(soup):
    """Extract available filter options from the page"""
    filters = {
        'units': [],  # bid - hunting units (Поделение)
        'users': []   # cid - users/operators (Ползвател)
    }
    
    # Look for select dropdowns or filter options
    # The actual implementation depends on the HTML structure
    # From the search results, I can see there are dropdowns for filtering
    
    # Try to find the unit filter dropdown
    unit_select = soup.find('select', {'name': re.compile(r'bid|unit|podelenie', re.I)})
    if unit_select:
        for option in unit_select.find_all('option'):
            value = option.get('value', '')
            text = option.get_text(strip=True)
            if value and text and value != '0':
                filters['units'].append({'id': value, 'name': text})
    
    # Try to find the user/operator filter dropdown
    user_select = soup.find('select', {'name': re.compile(r'cid|user|client|polzvatel', re.I)})
    if user_select:
        for option in user_select.find_all('option'):
            value = option.get('value', '')
            text = option.get_text(strip=True)
            if value and text and value != '0':
                filters['users'].append({'id': value, 'name': text})
    
    # Alternative: Look for links with filter parameters
    if not filters['units']:
        for link in soup.find_all('a', href=True):
            if 'bid=' in link['href']:
                parsed = urlparse(link['href'])
                params = parse_qs(parsed.query)
                if 'bid' in params and params['bid'][0]:
                    bid_value = params['bid'][0]
                    text = link.get_text(strip=True)
                    if text and {'id': bid_value, 'name': text} not in filters['units']:
                        filters['units'].append({'id': bid_value, 'name': text})
    
    if not filters['users']:
        for link in soup.find_all('a', href=True):
            if 'cid=' in link['href']:
                parsed = urlparse(link['href'])
                params = parse_qs(parsed.query)
                if 'cid' in params and params['cid'][0]:
                    cid_value = params['cid'][0]
                    text = link.get_text(strip=True)
                    if text and {'id': cid_value, 'name': text} not in filters['users']:
                        filters['users'].append({'id': cid_value, 'name': text})
    
    return filters

def extract_pagination_info(soup):
    """Extract max offset from pagination (offset-based, not page-based)"""
    max_offset = 0
    
    # Look for pagination links - the page param is actually an OFFSET (0, 50, 100, 150...)
    pagination = soup.find_all('a', href=re.compile(r'page=\d+'))
    for link in pagination:
        href = link.get('href', '')
        match = re.search(r'page=(\d+)', href)
        if match:
            offset = int(match.group(1))
            max_offset = max(max_offset, offset)
    
    # Also check for "Last" link - this gives us the final offset
    last_link = soup.find('a', string=re.compile(r'Last|Последна|›', re.I))
    if last_link and last_link.get('href'):
        match = re.search(r'page=(\d+)', last_link['href'])
        if match:
            max_offset = max(max_offset, int(match.group(1)))
    
    return max_offset

def extract_hunt_marks(soup):
    """Extract hunt mark records from the table"""
    records = []
    
    # Find the main data table
    # Look for table with hunt marks data
    table = soup.find('table')
    if not table:
        return records
    
    # Get all rows (skip header)
    rows = table.find_all('tr')
    
    for row in rows[1:]:  # Skip header row
        cells = row.find_all(['td', 'th'])
        
        if len(cells) >= 6:  # We expect at least 6 columns
            record = {
                'unit': cells[0].get_text(strip=True),           # Поделение
                'user': cells[1].get_text(strip=True),           # Ползвател
                'mark': cells[2].get_text(strip=True),           # Марка
                'gender_age': cells[3].get_text(strip=True),     # Пол/Възраст
                'game_type': cells[4].get_text(strip=True),      # Дивеч
                'date': cells[5].get_text(strip=True)            # Дата
            }
            
            # Only add if we have meaningful data
            if record['mark'] and record['date']:
                records.append(record)
    
    return records

def scrape_all_hunt_marks():
    """Main scraping function"""
    print("=" * 60)
    print("🦌 SCDP Hunt Marks Scraper")
    print("=" * 60)
    
    all_records = []
    filters = {'units': [], 'users': []}
    
    # Fetch the first page to get filters and pagination info
    print("\n📄 Fetching main page...")
    response = fetch_page(BASE_URL)
    
    if not response:
        print("❌ Failed to fetch main page")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract filters
    print("\n🔍 Extracting filters...")
    filters = extract_filters(soup)
    print(f"  Found {len(filters['units'])} hunting units")
    print(f"  Found {len(filters['users'])} users/operators")
    
    # Extract pagination info (offset-based: 0, 50, 100, 150...)
    print("\n📖 Checking pagination...")
    max_offset = extract_pagination_info(soup)
    page_size = 50
    total_pages = (max_offset // page_size) + 1 if max_offset > 0 else 1
    print(f"  Max offset: {max_offset}")
    print(f"  Total pages: {total_pages}")
    
    # Extract records from first page
    records = extract_hunt_marks(soup)
    all_records.extend(records)
    print(f"  Page 1 (offset 0): Found {len(records)} records")
    
    # Fetch remaining pages using OFFSET-based pagination
    if max_offset > 0:
        print(f"\n📚 Fetching pages 2-{total_pages}...")
        for page_num in range(2, total_pages + 1):
            offset = (page_num - 1) * page_size
            params = {'page': offset}
            response = fetch_page(BASE_URL, params=params)
            
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                records = extract_hunt_marks(soup)
                all_records.extend(records)
                print(f"  Page {page_num} (offset {offset}): Found {len(records)} records")
                
                # Be respectful - don't hammer the server
                time.sleep(1)
            else:
                print(f"  Page {page_num} (offset {offset}): Failed to fetch")
                
            # Stop if we got no records (we've reached the end)
            if len(records) == 0:
                print(f"  No more records, stopping at page {page_num}")
                break
    
    # Compile final data structure
    data = {
        'scrape_date': datetime.now().isoformat(),
        'source_url': BASE_URL,
        'total_records': len(all_records),
        'filters': filters,
        'records': all_records
    }
    
    return data

def save_data(data):
    """Save data to JSON file"""
    if not data:
        print("\n❌ No data to save")
        return False
    
    print(f"\n💾 Saving data to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {data['total_records']} records")
        return True
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return False

def main():
    """Main entry point"""
    data = scrape_all_hunt_marks()
    
    if data:
        save_data(data)
        
        print("\n" + "=" * 60)
        print("✅ Scraping complete!")
        print("=" * 60)
        print(f"📊 Statistics:")
        print(f"   Total records: {data['total_records']}")
        print(f"   Hunting units: {len(data['filters']['units'])}")
        print(f"   Users/Operators: {len(data['filters']['users'])}")
        print(f"   Scraped: {data['scrape_date']}")
        print("=" * 60)
    else:
        print("\n❌ Scraping failed")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

