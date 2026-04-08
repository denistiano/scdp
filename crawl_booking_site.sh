#!/bin/bash

# Enhanced crawler for scdp.bg/booking with PROPER extraction
# Uses HTTPS and extracts correct titles from HTML

BASE_URL="https://scdp.bg/booking"
OUTPUT_JSON="booking_content.json"
IMAGES_DIR="booking_images"
FILES_DIR="booking_files"

mkdir -p "$IMAGES_DIR" "$FILES_DIR"

echo "🔍 Enhanced crawling with HTTPS..."

# Function to escape JSON
escape_json() {
    printf '%s' "$1" | jq -Rs .
}

# Function to normalize URL
normalize_url() {
    local url="$1"
    if [[ "$url" =~ ^https?:// ]]; then
        echo "$url"
    elif [[ "$url" =~ ^/ ]]; then
        echo "https://scdp.bg${url}"
    else
        echo "${BASE_URL}/${url}"
    fi
}

# Function to download image
download_image() {
    local img_url="$1"
    local img_name=$(basename "$img_url" | sed 's/[?#].*//')
    local img_path="${IMAGES_DIR}/${img_name}"
    
    if [[ ! -f "$img_path" ]] && [[ ! "$img_url" =~ (horns\.png)$ ]]; then
        curl -sL --max-time 10 -o "$img_path" "$img_url" 2>/dev/null || true
    fi
    
    echo "$img_path"
}

# Function to extract title from listing page
extract_list_title() {
    local html="$1"
    local url="$2"
    
    # Extract from <span class="title">
    local title=$(echo "$html" | grep -oP '<span class="title">\K[^<]+' | head -1 || echo "")
    
    if [[ -n "$title" ]]; then
        echo "$title"
        return
    fi
    
    # Fallback: extract from URL
    local path_part=$(echo "$url" | sed 's/.*\///' | sed 's/-[0-9]*$//' | sed 's/-/ /g')
    echo "$path_part"
}

# Fetch homepage
echo "📥 Fetching site pages..."
INDEX_HTML=$(curl -sL --max-time 10 "$BASE_URL")

# Fetch listing pages to get proper titles
echo "📥 Fetching hotels list..."
HOTELS_HTML=$(curl -sL --max-time 10 "$BASE_URL/hotels")

echo "📥 Fetching services list..."
SERVICES_HTML=$(curl -sL --max-time 10 "$BASE_URL/services")

echo "📥 Fetching news list..."
NEWS_HTML=$(curl -sL --max-time 10 "$BASE_URL/news")

# Extract all links
LINKS=$(echo "$INDEX_HTML" | grep -oP 'href=["'"'"']\K[^"'"'"']+' | sort -u)

# Build page list
declare -a ALL_PAGES
ALL_PAGES+=("$BASE_URL")

while IFS= read -r link; do
    [[ -z "$link" ]] && continue
    [[ "$link" =~ ^# ]] && continue
    [[ "$link" =~ ^mailto: ]] && continue
    [[ "$link" =~ ^tel: ]] && continue
    [[ "$link" =~ ^javascript: ]] && continue
    [[ "$link" =~ \.(css|js|pdf|png|jpg|jpeg|gif|svg)(\?|$) ]] && continue
    
    full_url=$(normalize_url "$link")
    
    if [[ "$full_url" =~ ^https://scdp\.bg/booking ]]; then
        ALL_PAGES+=("$full_url")
    fi
done <<< "$LINKS"

# Remove duplicates
IFS=$'\n' ALL_PAGES=($(printf "%s\n" "${ALL_PAGES[@]}" | sort -u))

echo "📄 Found ${#ALL_PAGES[@]} pages"

# Download PDFs
for page_url in "${ALL_PAGES[@]}"; do
    if [[ "$page_url" =~ \.pdf$ ]]; then
        echo "📎 Downloading PDF..."
        filename=$(basename "$page_url")
        curl -sL --max-time 30 -o "${FILES_DIR}/$filename" "$page_url"
    fi
done

# Start JSON
echo '{' > "$OUTPUT_JSON"
echo '  "site_url": "'$BASE_URL'",' >> "$OUTPUT_JSON"
echo '  "pages": [' >> "$OUTPUT_JSON"

FIRST_PAGE=true
for page_url in "${ALL_PAGES[@]}"; do
    # Skip non-HTML
    if [[ "$page_url" =~ \.(css|js|pdf|png|jpg|jpeg|gif|svg)$ ]]; then
        continue
    fi
    
    echo "🔍 $page_url"
    
    PAGE_HTML=$(curl -sL --max-time 10 "$page_url" 2>/dev/null || echo "")
    
    if [[ -z "$PAGE_HTML" ]]; then
        continue
    fi
    
    # Extract title from listing pages first
    PAGE_TITLE=""
    if [[ "$page_url" =~ /hotels/ ]]; then
        # Try to find title in hotels list HTML
        HOTEL_SLUG=$(echo "$page_url" | sed 's/.*hotels\///')
        PAGE_TITLE=$(echo "$HOTELS_HTML" | grep -B5 "href=\"hotels/$HOTEL_SLUG\"" | grep -oP '<span class="title">\K[^<]+' | head -1 || echo "")
    elif [[ "$page_url" =~ /services/ ]]; then
        SERVICE_SLUG=$(echo "$page_url" | sed 's/.*services\///')
        PAGE_TITLE=$(echo "$SERVICES_HTML" | grep -B5 "href=\"services/$SERVICE_SLUG\"" | grep -oP '<span class="title">\K[^<]+' | head -1 || echo "")
    elif [[ "$page_url" =~ /news/ ]]; then
        NEWS_SLUG=$(echo "$page_url" | sed 's/.*news\///')
        PAGE_TITLE=$(echo "$NEWS_HTML" | grep -B5 "href=\"news/$NEWS_SLUG\"" | grep -oP 'class="article-title"[^>]*>\s*<a[^>]*>\K[^<]+' | head -1 || echo "")
    fi
    
    # Fallback: use page title tag
    if [[ -z "$PAGE_TITLE" ]]; then
        PAGE_TITLE=$(echo "$PAGE_HTML" | grep -oP '<title>\K[^<]+' | head -1 | sed 's/&[^;]*;//g')
    fi
    
    # Extract ALL content from main content area (not just paragraphs)
    # Get content from div.content, div.content-part, div.service-desc
    CONTENT_HTML=$(echo "$PAGE_HTML" | grep -oP '<div class="(content|content-part|service-desc|hotel-desc)"[^>]*>.*?</div>' | head -1)
    
    # Extract all paragraphs from content area
    PARAS=$(echo "$PAGE_HTML" | grep -oP '<p[^>]*>\K.*?(?=</p>)' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/&quot;/"/g' | sed 's/&#039;/'"'"'/g' | sed 's/&[^;]*;//g' | \
            grep -v "гр. Габрово 5300" | grep -v "Работно време" | grep -v "Свържете се с нас" | grep -v "^$" | sort -u | head -30)
    
    # Extract ALL lists (ul/li) for features/details
    LISTS=$(echo "$PAGE_HTML" | grep -oP '<li[^>]*>\K[^<]+' | sed 's/&nbsp;/ /g' | sed 's/&[^;]*;//g' | grep -v "^$" | sort -u)
    
    # Combine paragraphs and lists into full content
    ALL_CONTENT=$(echo -e "$PARAS\n$LISTS")
    
    PARA_ARRAY="["
    FIRST_PARA=true
    while IFS= read -r para; do
        [[ -z "$para" ]] && continue
        [[ ${#para} -lt 30 ]] && continue
        [[ "$para" =~ ^(ЛОВ|УСЛУГИ|НАСТАНЯВАНЕ|ТУРИЗЪМ|НАЧАЛО)$ ]] && continue
        [[ "$para" =~ ^(Български|English|Виж всички)$ ]] && continue
        
        if [[ "$FIRST_PARA" == true ]]; then
            FIRST_PARA=false
        else
            PARA_ARRAY+=","
        fi
        PARA_ARRAY+=$(escape_json "$para")
    done <<< "$ALL_CONTENT"
    PARA_ARRAY+="]"
    
    # Extract ALL images including gallery images (prioritize larger sizes)
    # Look for data-lightbox and href links to full-size images
    GALLERY_IMAGES=$(echo "$PAGE_HTML" | grep -oP 'href=["'"'"']\K[^"'"'"']+(?=["'"'"'][^>]*data-lightbox)' | grep -E '\.(jpg|jpeg|png|gif)')
    
    # Also get regular image sources
    SRC_IMAGES=$(echo "$PAGE_HTML" | grep -oP 'src=["'"'"']\K[^"'"'"']+' | grep -E '\.(jpg|jpeg|png|gif)' | grep -v -E '(logo-scdp|horns\.png|_87x65)')
    
    # Combine and prioritize larger images (800x600, 220x125 over thumbnails)
    ALL_IMAGES=$(echo -e "$GALLERY_IMAGES\n$SRC_IMAGES" | grep -E '(_800x600|_220x125|_190x142)' | sort -u)
    if [[ -z "$ALL_IMAGES" ]]; then
        ALL_IMAGES=$(echo -e "$GALLERY_IMAGES\n$SRC_IMAGES" | sort -u)
    fi
    
    IMAGE_ARRAY="["
    FIRST_IMG=true
    IMG_COUNT=0
    while IFS= read -r img_url && [[ $IMG_COUNT -lt 20 ]]; do
        [[ -z "$img_url" ]] && continue
        [[ "$img_url" =~ (logo-scdp|horns\.png|_87x65) ]] && continue
        
        full_img_url=$(normalize_url "$img_url")
        local_path=$(download_image "$full_img_url")
        
        if [[ "$FIRST_IMG" == true ]]; then
            FIRST_IMG=false
        else
            IMAGE_ARRAY+=","
        fi
        
        IMAGE_ARRAY+='{"url":'$(escape_json "$full_img_url")',"local_path":'$(escape_json "$local_path")'}'
        ((IMG_COUNT++))
    done <<< "$ALL_IMAGES"
    IMAGE_ARRAY+="]"
    
    # Add comma if not first page
    if [[ "$FIRST_PAGE" == true ]]; then
        FIRST_PAGE=false
    else
        echo ',' >> "$OUTPUT_JSON"
    fi
    
    # Write page data
    echo '    {' >> "$OUTPUT_JSON"
    echo '      "url": '$(escape_json "$page_url")',' >> "$OUTPUT_JSON"
    echo '      "title": '$(escape_json "$PAGE_TITLE")',' >> "$OUTPUT_JSON"
    echo "      \"paragraphs\": $PARA_ARRAY," >> "$OUTPUT_JSON"
    echo "      \"images\": $IMAGE_ARRAY" >> "$OUTPUT_JSON"
    echo -n '    }' >> "$OUTPUT_JSON"
done

# Close JSON
echo '' >> "$OUTPUT_JSON"
echo '  ]' >> "$OUTPUT_JSON"
echo '}' >> "$OUTPUT_JSON"

# Download logos
echo "📥 Downloading logos..."
LOGO_URL="https://scdp.bg/booking/assets/img/logo-scdp-bg.png"
LOGO_MOBILE_URL="https://scdp.bg/assets/theme/images/logo/logo-left.png"

curl -sL --max-time 10 -o "$IMAGES_DIR/logo-scdp-bg.png" "$LOGO_URL" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Desktop logo downloaded"
else
    echo "⚠ Desktop logo download failed"
fi

curl -sL --max-time 10 -o "$IMAGES_DIR/logo-mobile.png" "$LOGO_MOBILE_URL" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Mobile logo downloaded"
else
    echo "⚠ Mobile logo download failed"
fi

echo "✅ Enhanced crawling complete!"

# Validate
if command -v jq &> /dev/null; then
    if jq empty "$OUTPUT_JSON" 2>/dev/null; then
        PAGE_COUNT=$(jq '.pages | length' "$OUTPUT_JSON")
        echo "✓ Valid JSON with $PAGE_COUNT pages"
    else
        echo "✗ JSON validation failed"
    fi
fi

