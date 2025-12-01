#!/bin/bash

# Download free hunting/nature images from Unsplash
IMAGES_DIR="hunting_hero_images"
mkdir -p "$IMAGES_DIR"

echo "Downloading professional hunting/nature images..."

# High quality hunting and nature images from Unsplash
declare -A IMAGES=(
    ["forest-path.jpg"]="https://images.unsplash.com/photo-1448375240586-882707db888b"
    ["deer-forest.jpg"]="https://images.unsplash.com/photo-1547481887-a26e2cacb3ad"
    ["hunting-lodge.jpg"]="https://images.unsplash.com/photo-1580587771525-78b9dba3b914"
    ["forest-lake.jpg"]="https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
    ["mountain-view.jpg"]="https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
    ["wild-deer.jpg"]="https://images.unsplash.com/photo-1484406566174-9da000fda645"
    ["forest-cabin.jpg"]="https://images.unsplash.com/photo-1587061949409-02df41d5e562"
    ["autumn-forest.jpg"]="https://images.unsplash.com/photo-1476231682828-37e571bc172f"
)

for filename in "${!IMAGES[@]}"; do
    url="${IMAGES[$filename]}"
    echo "Downloading $filename..."
    curl -s -L "${url}?w=1920&q=85" -o "$IMAGES_DIR/$filename"
done

echo "✓ Downloaded ${#IMAGES[@]} images to $IMAGES_DIR/"



