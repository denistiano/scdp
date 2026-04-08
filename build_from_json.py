#!/usr/bin/env python3
"""
Modern Hunting & Tourism Website Builder - v2
With modals, better images, and improved UX
"""

import json
import os
import shutil
from pathlib import Path
from urllib.parse import urlparse
import html as html_lib
import re

# Configuration
JSON_FILE = "booking_content.json"
OUTPUT_DIR = "website"

def clean_directories():
    """Remove old website and create fresh structure"""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    for dir_path in [OUTPUT_DIR, f"{OUTPUT_DIR}/assets/css", f"{OUTPUT_DIR}/assets/js",
                     f"{OUTPUT_DIR}/images", f"{OUTPUT_DIR}/files"]:
        os.makedirs(dir_path, exist_ok=True)

def copy_assets():
    """Copy all extracted assets"""
    print("📁 Copying assets...")
    
    # Copy booking images (filter out tiny thumbnails)
    if os.path.exists("booking_images"):
        for img in os.listdir("booking_images"):
            # Skip tiny thumbnail images
            if '_87x65' in img or '_65x87' in img:
                continue
            src = os.path.join("booking_images", img)
            if os.path.isfile(src):
                shutil.copy2(src, f"{OUTPUT_DIR}/images/{img}")
    
    # Copy hero images
    if os.path.exists("hunting_hero_images"):
        for img in os.listdir("hunting_hero_images"):
            src = os.path.join("hunting_hero_images", img)
            if os.path.isfile(src):
                shutil.copy2(src, f"{OUTPUT_DIR}/images/{img}")
    
    # Copy files
    if os.path.exists("booking_files"):
        for file in os.listdir("booking_files"):
            src = os.path.join("booking_files", file)
            if os.path.isfile(src):
                shutil.copy2(src, f"{OUTPUT_DIR}/files/{file}")

def create_modern_css():
    """Generate modern CSS with modals"""
    css = """
/* Modern Hunting & Tourism Website - 2024 */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #2d4a1e;
    --secondary: #5a7f3a;
    --accent: #d4a373;
    --dark: #1a1a1a;
    --light: #f8f6f3;
    --white: #ffffff;
    --text: #2c2c2c;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    overflow-x: hidden;
    -webkit-text-size-adjust: 100%;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: var(--text);
    background: var(--white);
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    line-height: 1.2;
}

/* Top Bar */
.top-bar {
    background: var(--dark);
    color: white;
    padding: 12px 0;
    font-size: 14px;
}

.top-bar .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top-bar a {
    color: var(--accent);
    text-decoration: none;
}

/* Header */
header {
    background: #f5f9ed;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 3px solid var(--secondary);
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 15px;
    text-decoration: none;
    max-width: 100%;
    overflow: hidden;
}

.logo img {
    height: 60px;
    max-width: 100%;
    width: auto;
    object-fit: contain;
}

.logo-mobile {
    display: none;
}

.logo-desktop {
    display: block;
}

.logo-text h1 {
    font-size: 22px;
    color: var(--primary);
    font-family: Georgia, serif;
    margin-bottom: 2px;
}

.logo-text p {
    font-size: 11px;
    color: #d4a800;
    font-weight: 600;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 35px;
}

nav a {
    color: var(--dark);
    text-decoration: none;
    font-weight: 500;
    padding: 8px 0;
    border-bottom: 2px solid transparent;
    transition: all 0.3s;
    font-size: 15px;
}

nav a:hover, nav a.active {
    color: var(--secondary);
    border-bottom-color: var(--accent);
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 10px;
    z-index: 1001;
}

.hamburger {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.hamburger span {
    display: block;
    width: 28px;
    height: 3px;
    background: var(--primary);
    border-radius: 2px;
    transition: all 0.3s ease;
}

.mobile-menu-toggle.active .hamburger span:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
}

.mobile-menu-toggle.active .hamburger span:nth-child(2) {
    opacity: 0;
}

.mobile-menu-toggle.active .hamburger span:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
}

/* Hero Section */
.hero {
    position: relative;
    height: 50vh;
    min-height: 400px;
    max-height: 500px;
    max-width: 100vw;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(45,74,30,0.85), rgba(90,127,58,0.7));
}

.hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 900px;
    padding: 0 30px;
}

.hero h1 {
    font-size: 64px;
    margin-bottom: 20px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}

.hero p {
    font-size: 22px;
    margin-bottom: 30px;
    opacity: 0.95;
}

/* Page Hero (smaller for internal pages) */
.page-hero {
    position: relative;
    height: 200px;
    max-height: 250px;
    max-width: 100vw;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-bottom: 60px;
}

.page-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(45,74,30,0.8), rgba(90,127,58,0.6));
}

.page-hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
}

.page-hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.page-hero p {
    font-size: 18px;
    opacity: 0.9;
}

.btn {
    display: inline-block;
    padding: 16px 40px;
    background: var(--accent);
    color: var(--dark);
    text-decoration: none;
    font-weight: 600;
    border-radius: 50px;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 14px;
    border: none;
    cursor: pointer;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    background: #e0b585;
}

.btn-secondary {
    background: var(--primary);
    border: 2px solid var(--primary);
    color: white;
}

.btn-secondary:hover {
    background: var(--secondary);
    border-color: var(--secondary);
    color: white;
}

/* Container */
.container {
    max-width: 1400px;
    width: 100%;
    margin: 0 auto;
    padding: 0 30px;
    box-sizing: border-box;
}

/* Sections */
section {
    padding: 80px 0;
}

.section-header {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 60px;
}

.section-header h2 {
    font-size: 42px;
    color: var(--primary);
    margin-bottom: 15px;
}

.section-header p {
    font-size: 18px;
    color: #666;
}

/* Cards Grid */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 40px;
}

.card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s;
    cursor: pointer;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-image {
    position: relative;
    height: 280px;
    overflow: hidden;
}

.card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s;
}

.card:hover .card-image img {
    transform: scale(1.1);
}

.card-badge {
    position: absolute;
    top: 20px;
    left: 20px;
    background: var(--accent);
    color: var(--dark);
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-body {
    padding: 30px;
}

.card h3 {
    font-size: 24px;
    color: var(--primary);
    margin-bottom: 15px;
}

.card p {
    color: #666;
    margin-bottom: 20px;
    line-height: 1.6;
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.7);
    animation: fadeIn 0.3s;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    background-color: white;
    margin: 3% auto;
    width: 90%;
    max-width: 1000px;
    border-radius: 12px;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideDown 0.3s;
    position: relative;
}

@keyframes slideDown {
    from {
        transform: translateY(-50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.modal-header {
    position: relative;
    height: 300px;
    max-width: 100%;
    background-size: cover;
    background-position: center;
    border-radius: 12px 12px 0 0;
    overflow: hidden;
}

.modal-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.7));
}

.modal-header h2 {
    position: absolute;
    bottom: 30px;
    left: 40px;
    right: 40px;
    color: white;
    font-size: 36px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.modal-close {
    position: absolute;
    top: 10px;
    right: 10px;
    color: white;
    font-size: 35px;
    font-weight: bold;
    cursor: pointer;
    background: rgba(0,0,0,0.8);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    z-index: 2001;
    line-height: 1;
}

.modal-close:hover {
    background: rgba(0,0,0,0.95);
    transform: rotate(90deg);
}

@media (max-width: 768px) {
    .modal-close {
        position: fixed;
        top: 5px;
        right: 5px;
        width: 40px;
        height: 40px;
        font-size: 30px;
    }
}

.modal-body {
    padding: 40px;
}

.modal-body p {
    margin-bottom: 20px;
    font-size: 17px;
    line-height: 1.8;
    text-align: justify;
}

.modal-images {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    margin: 30px 0;
}

.modal-images img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.3s;
}

.modal-images img:hover {
    transform: scale(1.05);
}

/* Lightbox Gallery */
.lightbox {
    display: none;
    position: fixed;
    z-index: 3000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.95);
    animation: fadeIn 0.3s;
}

.lightbox-content {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px;
}

.lightbox-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
}

.lightbox-close {
    position: fixed;
    top: 10px;
    right: 10px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    background: rgba(255,255,255,0.2);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    z-index: 3001;
    line-height: 1;
}

.lightbox-close:hover {
    background: rgba(255,255,255,0.3);
    transform: rotate(90deg);
}

.lightbox-nav {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    color: white;
    font-size: 50px;
    font-weight: bold;
    cursor: pointer;
    background: rgba(255,255,255,0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    user-select: none;
}

.lightbox-nav:hover {
    background: rgba(255,255,255,0.2);
}

.lightbox-prev {
    left: 20px;
}

.lightbox-next {
    right: 20px;
}

.lightbox-counter {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 18px;
    background: rgba(0,0,0,0.5);
    padding: 10px 20px;
    border-radius: 25px;
}

@media (max-width: 768px) {
    .lightbox-content {
        padding: 20px;
    }
    .lightbox-close {
        top: 5px;
        right: 5px;
        width: 40px;
        height: 40px;
        font-size: 30px;
    }
    .lightbox-nav {
        width: 40px;
        height: 40px;
        font-size: 25px;
    }
    .lightbox-prev {
        left: 5px;
    }
    .lightbox-next {
        right: 5px;
    }
}

.modal-footer {
    padding: 30px 40px;
    background: var(--light);
    border-radius: 0 0 12px 12px;
    display: flex;
    gap: 15px;
    justify-content: center;
}

/* Footer */
footer {
    background: var(--dark);
    color: white;
    padding: 60px 0 30px;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 50px;
    margin-bottom: 40px;
}

.footer-section h3 {
    color: var(--accent);
    margin-bottom: 20px;
    font-size: 20px;
}

.footer-section p,
.footer-section a {
    color: #ccc;
    text-decoration: none;
    display: block;
    margin-bottom: 10px;
}

.footer-section a:hover {
    color: white;
}

.footer-bottom {
    text-align: center;
    padding-top: 30px;
    border-top: 1px solid #333;
    color: #999;
}

/* Responsive */
@media (max-width: 1024px) {
    .hero h1 { font-size: 48px; }
    .page-hero h1 { font-size: 32px; }
    .cards-grid { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
}

@media (max-width: 768px) {
    .hero { 
        height: 40vh;
        min-height: 300px;
        max-height: 400px;
    }
    .hero h1 { font-size: 28px; }
    .hero p { font-size: 16px; }
    
    .page-hero {
        height: 150px;
        max-height: 180px;
    }
    .page-hero h1 { font-size: 24px; }
    
    .header-content {
        flex-direction: row;
        justify-content: space-between;
        text-align: left;
    }
    
    .logo-desktop {
        display: none;
    }
    
    .logo-mobile {
        display: block;
    }
    
    .logo img {
        height: 50px;
    }
    
    .mobile-menu-toggle {
        display: block;
    }
    
    nav {
        position: fixed;
        top: 0;
        right: -100%;
        width: 280px;
        height: 100vh;
        background: white;
        box-shadow: -5px 0 25px rgba(0,0,0,0.2);
        transition: right 0.3s ease;
        z-index: 1000;
        padding-top: 80px;
    }
    
    nav.mobile-open {
        right: 0;
    }
    
    nav ul {
        flex-direction: column;
        gap: 0;
        padding: 20px 0;
    }
    
    nav li {
        border-bottom: 1px solid #f0f0f0;
    }
    
    nav a {
        display: block;
        padding: 18px 30px;
        font-size: 16px;
        border-bottom: none;
    }
    
    nav a:hover, nav a.active {
        background: var(--light);
        border-bottom: none;
    }
    
    .cards-grid { grid-template-columns: 1fr; }
    .modal-content { width: 95%; margin: 5% auto; }
    .modal-body { padding: 25px; }
    section { padding: 60px 0; }
    
    /* Mobile overlay */
    .mobile-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    }
    
    .mobile-overlay.active {
        display: block;
    }
}
"""
    
    with open(f"{OUTPUT_DIR}/assets/css/style.css", "w", encoding="utf-8") as f:
        f.write(css.strip())

def create_js():
    """Generate JavaScript for modals and interactivity"""
    js = """
// Modern interactivity with modals
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileNav = document.getElementById('mobile-nav');
    const mobileOverlay = document.getElementById('mobile-overlay');
    
    if (mobileToggle && mobileNav && mobileOverlay) {
        mobileToggle.addEventListener('click', function() {
            mobileToggle.classList.toggle('active');
            mobileNav.classList.toggle('mobile-open');
            mobileOverlay.classList.toggle('active');
            document.body.style.overflow = mobileNav.classList.contains('mobile-open') ? 'hidden' : 'auto';
        });
        
        // Close menu when clicking overlay
        mobileOverlay.addEventListener('click', function() {
            mobileToggle.classList.remove('active');
            mobileNav.classList.remove('mobile-open');
            mobileOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
        
        // Close menu when clicking a link
        mobileNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                mobileToggle.classList.remove('active');
                mobileNav.classList.remove('mobile-open');
                mobileOverlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        });
    }
    
    // Modal functionality
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    };
    
    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
    
    // Escape key closes modal and lightbox
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            // Close modals
            document.querySelectorAll('.modal').forEach(modal => {
                modal.style.display = 'none';
            });
            // Close lightboxes
            document.querySelectorAll('.lightbox').forEach(lightbox => {
                lightbox.style.display = 'none';
            });
            document.body.style.overflow = 'auto';
        }
    });
    
    // Lightbox functionality
    window.openLightbox = function(modalId, index) {
        const lightboxId = 'lightbox-' + modalId;
        const lightbox = document.getElementById(lightboxId);
        if (lightbox) {
            const varName = modalId.replace(/-/g, '_');
            window['currentLightboxIndex_' + varName] = index;
            updateLightboxImage(modalId);
            lightbox.style.display = 'block';
        }
    };
    
    window.closeLightbox = function(modalId) {
        const lightboxId = 'lightbox-' + modalId;
        const lightbox = document.getElementById(lightboxId);
        if (lightbox) {
            lightbox.style.display = 'none';
        }
    };
    
    window.changeLightboxImage = function(modalId, direction) {
        const varName = modalId.replace(/-/g, '_');
        const images = window['galleryImages_' + varName];
        if (images) {
            let currentIndex = window['currentLightboxIndex_' + varName];
            currentIndex += direction;
            if (currentIndex < 0) currentIndex = images.length - 1;
            if (currentIndex >= images.length) currentIndex = 0;
            window['currentLightboxIndex_' + varName] = currentIndex;
            updateLightboxImage(modalId);
        }
    };
    
    function updateLightboxImage(modalId) {
        const varName = modalId.replace(/-/g, '_');
        const images = window['galleryImages_' + varName];
        const currentIndex = window['currentLightboxIndex_' + varName];
        
        if (images && currentIndex !== undefined) {
            const img = document.getElementById('lightbox-img-' + modalId);
            const counter = document.getElementById('lightbox-counter-' + modalId);
            if (img && images[currentIndex]) {
                img.src = images[currentIndex];
            }
            if (counter) {
                counter.textContent = (currentIndex + 1) + ' / ' + images.length;
            }
        }
    }
    
    // Keyboard navigation for lightbox
    document.addEventListener('keydown', function(event) {
        const openLightbox = document.querySelector('.lightbox[style*="display: block"]');
        if (openLightbox) {
            const modalId = openLightbox.id.replace('lightbox-', '');
            if (event.key === 'ArrowLeft') {
                changeLightboxImage(modalId, -1);
            } else if (event.key === 'ArrowRight') {
                changeLightboxImage(modalId, 1);
            }
        }
    });
    
    // Close lightbox when clicking outside image
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('lightbox')) {
            event.target.style.display = 'none';
        }
    });
    
    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Active navigation
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
"""
    
    with open(f"{OUTPUT_DIR}/assets/js/main.js", "w", encoding="utf-8") as f:
        f.write(js.strip())

def url_to_id(url):
    """Convert URL to modal ID"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    path = path.replace('booking/', '')
    return 'modal-' + path.replace('/', '-').replace('.', '-')

def get_best_image(images):
    """Get the best quality image (avoid tiny thumbnails)"""
    if not images:
        return ''
    
    # Filter out tiny images
    good_images = [img for img in images if '_87x65' not in img.get('local_path', '') and '_65x87' not in img.get('local_path', '')]
    
    if not good_images:
        return ''
    
    return good_images[0].get('local_path', '')

def extract_title_from_paragraphs(paragraphs, url):
    """Try to extract a meaningful title from first paragraph or URL"""
    # Hotel/Service name mapping from original website
    NAME_MAPPINGS = {
        'batakliiata-13': 'БАТАКЛИЯТА',
        'batin-14': 'БАТИН',
        'elen-18': 'ЕЛЕН',
        'fazan-17': 'ФАЗАН',
        'iri-hisar-20': 'ИРИ ХИСАР',
        'kokiche-19': 'КОКИЧЕ',
        'lugut-16': 'ЛЪГЪТ',
        'mlechevo-22': 'МЛЕЧЕВО',
        'voden-i-21': 'ВОДЕН I',
        'voden-ii-15': 'ВОДЕН II',
        'fotolov-32': 'Фотолов',
        'grupov-lov-na-diva-svinia-10': 'Групов лов на дива свиня',
        'grupov-lov-na-diva-svinia-lugut-17': 'Групов лов на дива свиня - Лъгът',
        'individualen-lov-na-diva-svinia-9': 'Индивидуален лов на дива свиня',
        'individualen-lov-na-diva-svinia-lugut-16': 'Индивидуален лов на дива свиня - Лъгът',
        'lov-na-blagoroden-elen-25': 'Лов на благороден елен',
        'lov-na-blagoroden-elen-lugut-14': 'Лов на благороден елен - Лъгът',
        'lov-na-elen-lopatar-11': 'Лов на елен лопатар',
        'lov-na-fazan-i-dreben-divech-21': 'Лов на фазан и дребен дивеч',
        'lov-na-srundak-2': 'Лов на сръндак',
        'lov-na-srundak-lugut-15': 'Лов на сръндак - Лъгът',
        'obuchenie-na-lovni-kucheta-za-dreben-divech-23': 'Обучение на ловни кучета за дребен дивеч',
        'prodajba-na-divechovo-meso-33': 'Продажба на дивечово месо',
        'ribolov-24': 'Риболов',
    }
    
    # Parse from URL
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) > 1:
        title_part = path_parts[-1]
        
        # Check if we have a mapping (with the number)
        if title_part in NAME_MAPPINGS:
            return NAME_MAPPINGS[title_part]
        
        # Try without number
        title_part_no_num = re.sub(r'-\d+$', '', title_part)
        if title_part_no_num in NAME_MAPPINGS:
            return NAME_MAPPINGS[title_part_no_num]
    
    # Try to extract from first paragraph
    if paragraphs and len(paragraphs) > 0:
        first_para = paragraphs[0]
        # If first paragraph is short and mentions a location/name, use it
        if len(first_para) < 150 and ('ловен' in first_para.lower() or 'лов на' in first_para.lower()):
            return first_para
        
        # Try to find mentions of specific locations in text
        for location in ['Воден', 'Батин', 'Елен', 'Фазан', 'Кокиче', 'Лъгът', 'Батаклията', 'Ири Хисар']:
            if location in first_para:
                if '/hotels/' in url:
                    return f'Ловен дом {location}'
                break
    
    # Fallback
    if '/hotels/' in url:
        return 'Ловна хижа'
    elif '/services/' in url:
        return 'Ловна услуга'
    elif '/news/' in url:
        # For news, try to extract from first sentence
        if paragraphs and len(paragraphs) > 0:
            first_sent = paragraphs[0].split('.')[0]
            if len(first_sent) < 100:
                return first_sent
        return 'Новина'
    
    return ''

def categorize_pages(pages):
    """Organize pages by category"""
    categories = {
        'index': None,
        'hotels': [],
        'services': [],
        'news': [],
        'other': []
    }
    
    for page in pages:
        url = page['url']
        # Skip CSS files
        if '.css' in url or '.js' in url:
            continue
            
        if url.endswith('/booking') or url.endswith('/booking/'):
            categories['index'] = page
        elif '/hotels/' in url:
            # ALWAYS override with correct title from URL mapping
            page['title'] = extract_title_from_paragraphs(page.get('paragraphs', []), url)
            categories['hotels'].append(page)
        elif '/services/' in url:
            # ALWAYS override with correct title from URL mapping
            page['title'] = extract_title_from_paragraphs(page.get('paragraphs', []), url)
            categories['services'].append(page)
        elif '/news/' in url:
            # ALWAYS override with correct title from URL mapping
            page['title'] = extract_title_from_paragraphs(page.get('paragraphs', []), url)
            categories['news'].append(page)
        else:
            categories['other'].append(page)
    
    return categories

def generate_header():
    """Generate header with responsive logos"""
    return '''
    <div class="top-bar">
        <div class="container">
            <div>☎ 066/800-077 | ✉ <a href="mailto:booking@scdp.bg">booking@scdp.bg</a></div>
            <div>гр. Габрово | Работно време: Пн-Пт 8:30-17:00</div>
        </div>
    </div>
    <header>
        <div class="header-content">
            <a href="index.html" class="logo">
                <img src="images/logo-scdp-bg.png" alt="СЦДП" class="logo-desktop" onerror="this.style.display='none'">
                <img src="images/logo-mobile.png" alt="СЦДП" class="logo-mobile" onerror="this.style.display='none'">
            </a>
            <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Menu">
                <div class="hamburger">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </button>
            <nav id="mobile-nav">
                <ul>
                    <li><a href="index.html">Начало</a></li>
                    <li><a href="hotels.html">Настаняване</a></li>
                    <li><a href="services.html">Услуги</a></li>
                    <li><a href="news.html">Новини</a></li>
                    <li><a href="hunt-marks.html">Справка Отстрел</a></li>
                    <li><a href="contacts.html">Контакти</a></li>
                </ul>
            </nav>
        </div>
        <div class="mobile-overlay" id="mobile-overlay"></div>
    </header>
    '''

def generate_footer():
    """Generate footer"""
    return '''
    <footer id="contacts">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Контакти</h3>
                    <p>гр. Габрово 5300<br>
                    ул. „Бодра смяна" 3<br>
                    тел. 066 800 077<br>
                    e-mail: booking@scdp.bg</p>
                </div>
                <div class="footer-section">
                    <h3>Работно време</h3>
                    <p>Понеделник - Петък<br>
                    8:30 - 17:00 ч.</p>
                </div>
                <div class="footer-section">
                    <h3>Бързи връзки</h3>
                    <a href="hotels.html">Настаняване</a>
                    <a href="services.html">Услуги</a>
                    <a href="hunt-marks.html">Справка Отстрел</a>
                    <a href="files/hunt-season-2015.pdf" target="_blank">Ловен сезон 2015 (PDF)</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 СЦДП. Всички права запазени.</p>
            </div>
        </div>
    </footer>
    '''

def generate_modal(item, show_booking_buttons=True):
    """Generate modal for an item"""
    modal_id = url_to_id(item['url'])
    title = item.get('title', 'Детайли')
    paragraphs = item.get('paragraphs', [])
    images = item.get('images', [])
    
    # Get best hero image
    hero_image = get_best_image(images)
    hero_image_name = os.path.basename(hero_image) if hero_image else 'forest-path.jpg'
    
    # Content
    content_html = ''
    for para in paragraphs[:8]:
        if len(para) > 50:
            content_html += f'<p>{html_lib.escape(para)}</p>\n'
    
    # Images grid (skip tiny thumbnails)
    images_html = ''
    lightbox_html = ''
    good_images = [img for img in images if '_87x65' not in img.get('local_path', '')]
    if len(good_images) > 1:
        images_html = f'<div class="modal-images" id="gallery-{modal_id}">'
        image_urls = []
        for idx, img in enumerate(good_images[:8]):
            img_path = img.get('local_path', '')
            if img_path:
                img_name = os.path.basename(img_path)
                img_url = f'images/{img_name}'
                image_urls.append(img_url)
                images_html += f'<img src="{img_url}" alt="Image" onclick="openLightbox(\'{modal_id}\', {idx})">'
        images_html += '</div>'
        
        # Generate lightbox HTML
        modal_id_clean = modal_id.replace('-', '_')
        lightbox_html = f'''
        <div id="lightbox-{modal_id}" class="lightbox">
            <span class="lightbox-close" onclick="closeLightbox('{modal_id}')">&times;</span>
            <div class="lightbox-content">
                <span class="lightbox-nav lightbox-prev" onclick="changeLightboxImage('{modal_id}', -1)">&#10094;</span>
                <img id="lightbox-img-{modal_id}" class="lightbox-image" src="" alt="Gallery">
                <span class="lightbox-nav lightbox-next" onclick="changeLightboxImage('{modal_id}', 1)">&#10095;</span>
            </div>
            <div class="lightbox-counter" id="lightbox-counter-{modal_id}"></div>
        </div>
        <script>
            window.galleryImages_{modal_id_clean} = {json.dumps(image_urls)};
            window.currentLightboxIndex_{modal_id_clean} = 0;
        </script>
        '''
    
    # Conditional footer based on content type
    footer_html = ''
    if show_booking_buttons:
        footer_html = '''
            <div class="modal-footer">
                <a href="mailto:booking@scdp.bg" class="btn">Резервирай</a>
                <a href="tel:066800077" class="btn btn-secondary">Обади се</a>
            </div>
        '''
    else:
        footer_html = '''
            <div class="modal-footer">
                <a href="mailto:booking@scdp.bg" class="btn">Свържете се с нас</a>
            </div>
        '''
    
    return f'''
    <div id="{modal_id}" class="modal">
        <div class="modal-content">
            <div class="modal-header" style="background-image: url('images/{hero_image_name}')">
                <span class="modal-close" onclick="closeModal('{modal_id}')">&times;</span>
                <h2>{html_lib.escape(title)}</h2>
            </div>
            <div class="modal-body">
                {content_html}
                {images_html}
            </div>
            {footer_html}
        </div>
    </div>
    {lightbox_html}
    '''

def generate_card(item, badge_text):
    """Generate card for listing"""
    modal_id = url_to_id(item['url'])
    title = item.get('title', 'Услуга')
    images = item.get('images', [])
    image = get_best_image(images)
    image_name = os.path.basename(image) if image else 'forest-path.jpg'
    desc = item.get('paragraphs', [''])[0][:180] + '...' if item.get('paragraphs') else ''
    
    return f'''
    <div class="card" onclick="openModal('{modal_id}')">
        <div class="card-image">
            <img src="images/{image_name}" alt="{html_lib.escape(title)}">
            <div class="card-badge">{badge_text}</div>
        </div>
        <div class="card-body">
            <h3>{html_lib.escape(title)}</h3>
            <p>{html_lib.escape(desc)}</p>
            <a href="javascript:void(0)" class="btn">Виж повече</a>
        </div>
    </div>
    '''

def generate_index_page(categories):
    """Generate homepage - show only 3 per category"""
    hotels = categories['hotels'][:3]  # Only 3!
    services = categories['services'][:3]  # Only 3!
    
    hotels_html = ''.join([generate_card(h, 'Хижа') for h in hotels])
    hotels_modals = ''.join([generate_modal(h) for h in hotels])
    
    services_html = ''.join([generate_card(s, 'Услуга') for s in services])
    services_modals = ''.join([generate_modal(s) for s in services])
    
    html = f'''<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>СЦДП - Професионален лов и туризъм</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    {generate_header()}
    
    <div class="hero" style="background-image: url('images/forest-path.jpg')">
        <div class="hero-content">
            <h1>Професионален Лов<br>и Туризъм</h1>
            <p>Открийте най-добрите ловни дестинации и хижи в Северна България</p>
            <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                <a href="hotels.html" class="btn">Настаняване</a>
                <a href="services.html" class="btn btn-secondary">Услуги</a>
            </div>
        </div>
    </div>
    
    <section>
        <div class="container">
            <div class="section-header">
                <h2>Ловни хижи и настаняване</h2>
                <p>Комфортно настаняване в сърцето на природата</p>
            </div>
            <div class="cards-grid">
                {hotels_html}
            </div>
            <div style="text-align: center; margin-top: 40px;">
                <a href="hotels.html" class="btn">Всички хижи</a>
            </div>
        </div>
    </section>
    
    <section style="background: var(--light);">
        <div class="container">
            <div class="section-header">
                <h2>Ловни услуги</h2>
                <p>Разнообразие от ловни програми за всеки ловец</p>
            </div>
            <div class="cards-grid">
                {services_html}
            </div>
            <div style="text-align: center; margin-top: 40px;">
                <a href="services.html" class="btn">Всички услуги</a>
            </div>
        </div>
    </section>
    
    {generate_footer()}
    {hotels_modals}
    {services_modals}
    <script src="assets/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_contacts_page():
    """Generate modern contacts page"""
    html = '''<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Контакти - СЦДП</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .contact-hero {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 60px 30px;
            text-align: center;
        }
        .contact-hero h1 {
            font-size: 48px;
            margin-bottom: 15px;
        }
        .contact-hero p {
            font-size: 20px;
            opacity: 0.9;
        }
        .contact-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: -50px auto 60px;
            max-width: 1200px;
            padding: 0 30px;
        }
        .contact-card {
            background: white;
            padding: 40px 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            text-align: center;
            transition: transform 0.3s;
        }
        .contact-card:hover {
            transform: translateY(-10px);
        }
        .contact-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, var(--secondary), var(--primary));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 36px;
        }
        .contact-card h3 {
            color: var(--primary);
            font-size: 24px;
            margin-bottom: 20px;
        }
        .contact-card p {
            color: #666;
            line-height: 1.8;
            margin-bottom: 10px;
        }
        .contact-card a {
            color: var(--secondary);
            text-decoration: none;
            font-weight: 600;
        }
        .contact-card a:hover {
            color: var(--primary);
        }
        .info-section {
            background: var(--light);
            padding: 80px 30px;
            text-align: center;
        }
        .info-section h2 {
            font-size: 36px;
            color: var(--primary);
            margin-bottom: 30px;
        }
        .info-section p {
            max-width: 800px;
            margin: 0 auto 30px;
            font-size: 18px;
            line-height: 1.8;
            color: #555;
        }
    </style>
</head>
<body>
    ''' + generate_header() + '''
    
    <div class="contact-hero">
        <h1>Свържете се с нас</h1>
        <p>Готови сме да отговорим на вашите въпроси</p>
    </div>
    
    <div class="contact-cards">
        <div class="contact-card">
            <div class="contact-icon">📍</div>
            <h3>Адрес</h3>
            <p>гр. Габрово 5300<br>
            ул. „Бодра смяна" 3<br>
            <strong>Работно време:</strong><br>
            Понеделник - Петък<br>
            8:30 - 17:00 ч.</p>
        </div>
        
        <div class="contact-card">
            <div class="contact-icon">📞</div>
            <h3>Телефон & Факс</h3>
            <p><strong>Телефон:</strong><br>
            <a href="tel:066800077">066 800 077</a></p>
            <p><strong>Факс:</strong><br>
            066 800 094</p>
            <div style="margin-top: 25px;">
                <a href="tel:066800077" class="btn">Обадете се</a>
            </div>
        </div>
        
        <div class="contact-card">
            <div class="contact-icon">✉️</div>
            <h3>Email</h3>
            <p><strong>Офис:</strong><br>
            <a href="mailto:office@scdp.bg">office@scdp.bg</a></p>
            <p><strong>Резервации:</strong><br>
            <a href="mailto:booking@scdp.bg">booking@scdp.bg</a></p>
            <div style="margin-top: 25px;">
                <a href="mailto:booking@scdp.bg" class="btn">Изпратете запитване</a>
            </div>
        </div>
    </div>
    
    <div class="info-section">
        <div class="container">
            <h2>За Северноцентралното държавно предприятие</h2>
            <p>СЦДП управлява ловни територии в Североизточна България, включващи райони с богата фауна 
            и изключителни възможности за професионален лов. Предлагаме настаняване в комфортни ловни хижи, 
            професионални ловни програми и туристически маршрути.</p>
            <p>За повече информация посетете: 
            <a href="http://voden.bg" target="_blank" rel="noopener" style="color: var(--secondary); font-weight: 600;">voden.bg</a></p>
            <div style="margin-top: 40px;">
                <a href="files/hunt-season-2015.pdf" target="_blank" class="btn" style="font-size: 16px; padding: 18px 45px;">
                    📄 Ловен сезон 2015 (PDF)
                </a>
            </div>
        </div>
    </div>
    
    ''' + generate_footer() + '''
    
    <script src="assets/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_listing_page(items, title, description, badge_text, hero_bg, is_news=False):
    """Generate listing page with all items and modals"""
    cards_html = ''.join([generate_card(item, badge_text) for item in items])
    # For news, don't show booking buttons
    modals_html = ''.join([generate_modal(item, show_booking_buttons=not is_news) for item in items])
    
    html = f'''<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>{title} - СЦДП</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    {generate_header()}
    
    <div class="page-hero" style="background-image: url('images/{hero_bg}')">
        <div class="page-hero-content">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>
    
    <section>
        <div class="container">
            <div class="cards-grid">
                {cards_html}
            </div>
        </div>
    </section>
    
    {generate_footer()}
    {modals_html}
    <script src="assets/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_hunt_marks_page():
    """Generate hunt marks page from hunt_marks_data.json"""
    hunt_marks_file = "hunt_marks_data.json"
    
    # Check if hunt marks data exists
    if not os.path.exists(hunt_marks_file):
        print("⚠️  Hunt marks data not found, skipping hunt marks page")
        return False
    
    # Load hunt marks data
    with open(hunt_marks_file, 'r', encoding='utf-8') as f:
        hunt_data = json.load(f)
    
    # Get unique values for filters
    records = hunt_data.get('records', [])
    units = sorted(set(record.get('unit', '') for record in records))
    users = sorted(set(record.get('user', '') for record in records))
    game_types = sorted(set(record.get('game_type', '') for record in records))
    
    # Build filter options
    unit_options = ''.join(f'<option value="{u}">{html_lib.escape(u)}</option>' for u in units if u)
    user_options = ''.join(f'<option value="{u}">{html_lib.escape(u)}</option>' for u in users if u)
    game_options = ''.join(f'<option value="{g}">{html_lib.escape(g)}</option>' for g in game_types if g)
    
    # Format scrape date
    from datetime import datetime
    scrape_date = datetime.fromisoformat(hunt_data['scrape_date']).strftime('%d.%m.%Y %H:%M')
    
    # Embed the data directly in JavaScript
    records_json = json.dumps(records, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Справка Отстрел - СЦДП</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .hunt-marks-section {{
            padding: 40px 0 80px;
        }}
        .filters-panel {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }}
        .filters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .filter-group label {{
            font-weight: 600;
            color: var(--primary);
            font-size: 14px;
        }}
        .filter-group select, .filter-group input {{
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        .filter-group select:focus, .filter-group input:focus {{
            outline: none;
            border-color: var(--secondary);
        }}
        .filter-actions {{
            display: flex;
            gap: 15px;
            justify-content: flex-end;
            margin-top: 15px;
        }}
        .btn-filter {{
            padding: 10px 25px;
            background: var(--secondary);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .btn-filter:hover {{
            background: var(--primary);
            transform: translateY(-2px);
        }}
        .btn-reset {{
            padding: 10px 25px;
            background: transparent;
            color: var(--secondary);
            border: 2px solid var(--secondary);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .btn-reset:hover {{
            background: var(--secondary);
            color: white;
        }}
        .hunt-marks-table-wrapper {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .hunt-marks-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .hunt-marks-table thead {{
            background: var(--primary);
            color: white;
        }}
        .hunt-marks-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
            position: relative;
            transition: background 0.2s;
        }}
        .hunt-marks-table th:hover {{
            background: rgba(255,255,255,0.1);
        }}
        .hunt-marks-table th.sortable::after {{
            content: ' ⇅';
            opacity: 0.3;
            font-size: 12px;
        }}
        .hunt-marks-table th.sort-asc::after {{
            content: ' ▲';
            opacity: 1;
        }}
        .hunt-marks-table th.sort-desc::after {{
            content: ' ▼';
            opacity: 1;
        }}
        .hunt-marks-table tbody tr {{
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.2s;
        }}
        .hunt-marks-table tbody tr:hover {{
            background: #f8f9fa;
        }}
        .hunt-marks-table td {{
            padding: 12px 15px;
            font-size: 14px;
        }}
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .pagination-btn {{
            padding: 8px 15px;
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            font-size: 14px;
        }}
        .pagination-btn:hover {{
            background: var(--primary);
            color: white;
        }}
        .pagination-btn.active {{
            background: var(--secondary);
            border-color: var(--secondary);
            color: white;
        }}
        .pagination-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .pagination-info {{
            color: #666;
            font-size: 14px;
        }}
        .results-info {{
            padding: 15px 20px;
            background: var(--light);
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #666;
        }}
        .results-info strong {{
            color: var(--primary);
        }}
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}
        .no-results-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        @media (max-width: 768px) {{
            .hunt-marks-table-wrapper {{
                overflow-x: auto;
            }}
            .hunt-marks-table {{
                min-width: 600px;
            }}
            .filter-actions {{
                flex-direction: column;
            }}
            .btn-filter, .btn-reset {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    {generate_header()}
    
    <div class="page-hero" style="background-image: url('images/wild-deer.jpg')">
        <div class="page-hero-content">
            <h1>Справка Отстрел</h1>
            <p>Регистрирани ловни марки и отстрел на дивеч</p>
        </div>
    </div>
    
    <section class="hunt-marks-section">
        <div class="container">
            <div class="filters-panel">
                <h3 style="margin-bottom: 20px; color: var(--primary);">🔍 Филтриране</h3>
                <div class="filters-grid">
                    <div class="filter-group">
                        <label for="filter-unit">Поделение</label>
                        <select id="filter-unit">
                            <option value="">Всички</option>
                            {unit_options}
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="filter-user">Ползвател</label>
                        <select id="filter-user">
                            <option value="">Всички</option>
                            {user_options}
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="filter-game">Дивеч</label>
                        <select id="filter-game">
                            <option value="">Всички</option>
                            {game_options}
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="filter-search">Търсене</label>
                        <input type="text" id="filter-search" placeholder="Търсене по всички полета...">
                    </div>
                    <div class="filter-group">
                        <label for="filter-date-from">Дата от</label>
                        <input type="date" id="filter-date-from">
                    </div>
                    <div class="filter-group">
                        <label for="filter-date-to">Дата до</label>
                        <input type="date" id="filter-date-to">
                    </div>
                </div>
                <div class="filter-actions">
                    <button class="btn-reset" onclick="resetFilters()">Изчисти</button>
                    <button class="btn-filter" onclick="applyFilters()">Приложи</button>
                </div>
            </div>
            
            <div class="results-info" id="results-info">
                Показани записи <strong>1-50</strong> от общо <strong>{hunt_data['total_records']}</strong>
            </div>
            
            <div class="pagination" id="pagination-top">
                <!-- Populated by JavaScript -->
            </div>
            
            <div class="hunt-marks-table-wrapper">
                <table class="hunt-marks-table">
                    <thead>
                        <tr>
                            <th class="sortable" data-sort="unit" onclick="sortTable('unit')">Поделение</th>
                            <th class="sortable" data-sort="user" onclick="sortTable('user')">Ползвател</th>
                            <th class="sortable" data-sort="mark" onclick="sortTable('mark')">Марка</th>
                            <th class="sortable" data-sort="gender_age" onclick="sortTable('gender_age')">Пол/Възраст</th>
                            <th class="sortable" data-sort="game_type" onclick="sortTable('game_type')">Дивеч</th>
                            <th class="sortable" data-sort="date" onclick="sortTable('date')">Дата</th>
                        </tr>
                    </thead>
                    <tbody id="hunt-marks-tbody">
                        <!-- Populated by JavaScript -->
                    </tbody>
                </table>
            </div>
            
            <div class="pagination" id="pagination-bottom">
                <!-- Populated by JavaScript -->
            </div>
            
            <p style="text-align: center; color: #999; font-size: 13px; margin-top: 30px;">
                Последна актуализация: {scrape_date}
            </p>
        </div>
    </section>
    
    {generate_footer()}
    <script src="assets/js/main.js"></script>
    <script>
        const HUNT_MARKS_DATA = {records_json};
        
        let filteredData = [...HUNT_MARKS_DATA];
        let currentPage = 1;
        const recordsPerPage = 50;
        let currentSort = {{ field: 'date', order: 'desc' }};
        
        document.addEventListener('DOMContentLoaded', function() {{
            sortData();
            renderTable();
            renderPagination();
            updateResultsInfo();
            updateSortIndicators();
        }});
        
        function parseDate(dateStr) {{
            // Parse DD.MM.YYYY format
            const parts = dateStr.split('.');
            if (parts.length === 3) {{
                return new Date(parts[2], parts[1] - 1, parts[0]);
            }}
            return new Date(dateStr);
        }}
        
        function applyFilters() {{
            const unit = document.getElementById('filter-unit').value.toLowerCase();
            const user = document.getElementById('filter-user').value.toLowerCase();
            const gameType = document.getElementById('filter-game').value.toLowerCase();
            const searchTerm = document.getElementById('filter-search').value.toLowerCase();
            const dateFrom = document.getElementById('filter-date-from').value;
            const dateTo = document.getElementById('filter-date-to').value;
            
            filteredData = HUNT_MARKS_DATA.filter(record => {{
                const matchUnit = !unit || record.unit.toLowerCase().includes(unit);
                const matchUser = !user || record.user.toLowerCase().includes(user);
                const matchGame = !gameType || record.game_type.toLowerCase().includes(gameType);
                const matchSearch = !searchTerm || 
                    record.unit.toLowerCase().includes(searchTerm) ||
                    record.user.toLowerCase().includes(searchTerm) ||
                    record.mark.toLowerCase().includes(searchTerm) ||
                    record.game_type.toLowerCase().includes(searchTerm) ||
                    record.gender_age.toLowerCase().includes(searchTerm);
                
                let matchDate = true;
                if (dateFrom || dateTo) {{
                    const recordDate = parseDate(record.date);
                    if (dateFrom) {{
                        const fromDate = new Date(dateFrom);
                        matchDate = matchDate && recordDate >= fromDate;
                    }}
                    if (dateTo) {{
                        const toDate = new Date(dateTo);
                        toDate.setHours(23, 59, 59);
                        matchDate = matchDate && recordDate <= toDate;
                    }}
                }}
                
                return matchUnit && matchUser && matchGame && matchSearch && matchDate;
            }});
            
            sortData();
            currentPage = 1;
            renderTable();
            renderPagination();
            updateResultsInfo();
        }}
        
        function resetFilters() {{
            document.getElementById('filter-unit').value = '';
            document.getElementById('filter-user').value = '';
            document.getElementById('filter-game').value = '';
            document.getElementById('filter-search').value = '';
            document.getElementById('filter-date-from').value = '';
            document.getElementById('filter-date-to').value = '';
            
            filteredData = [...HUNT_MARKS_DATA];
            sortData();
            currentPage = 1;
            renderTable();
            renderPagination();
            updateResultsInfo();
        }}
        
        function sortTable(field) {{
            if (currentSort.field === field) {{
                currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
            }} else {{
                currentSort.field = field;
                currentSort.order = 'asc';
            }}
            
            sortData();
            currentPage = 1;
            renderTable();
            renderPagination();
            updateResultsInfo();
            updateSortIndicators();
        }}
        
        function sortData() {{
            filteredData.sort((a, b) => {{
                let aVal = a[currentSort.field];
                let bVal = b[currentSort.field];
                
                // Special handling for dates
                if (currentSort.field === 'date') {{
                    aVal = parseDate(aVal).getTime();
                    bVal = parseDate(bVal).getTime();
                }} else {{
                    // String comparison for other fields
                    aVal = String(aVal).toLowerCase();
                    bVal = String(bVal).toLowerCase();
                }}
                
                if (currentSort.order === 'asc') {{
                    return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
                }} else {{
                    return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
                }}
            }});
        }}
        
        function updateSortIndicators() {{
            document.querySelectorAll('.hunt-marks-table th').forEach(th => {{
                th.classList.remove('sort-asc', 'sort-desc');
                const sortField = th.getAttribute('data-sort');
                if (sortField === currentSort.field) {{
                    th.classList.add(currentSort.order === 'asc' ? 'sort-asc' : 'sort-desc');
                }}
            }});
        }}
        
        function renderTable() {{
            const tbody = document.getElementById('hunt-marks-tbody');
            tbody.innerHTML = '';
            
            const start = (currentPage - 1) * recordsPerPage;
            const end = start + recordsPerPage;
            const pageData = filteredData.slice(start, end);
            
            if (pageData.length === 0) {{
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="no-results">
                            <div class="no-results-icon">🔍</div>
                            <p>Не са намерени записи</p>
                        </td>
                    </tr>
                `;
                return;
            }}
            
            pageData.forEach(record => {{
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${{escapeHtml(record.unit)}}</td>
                    <td>${{escapeHtml(record.user)}}</td>
                    <td>${{escapeHtml(record.mark)}}</td>
                    <td>${{escapeHtml(record.gender_age)}}</td>
                    <td>${{escapeHtml(record.game_type)}}</td>
                    <td>${{escapeHtml(record.date)}}</td>
                `;
                tbody.appendChild(row);
            }});
        }}
        
        function renderPagination() {{
            const paginationTop = document.getElementById('pagination-top');
            const paginationBottom = document.getElementById('pagination-bottom');
            
            const totalPages = Math.ceil(filteredData.length / recordsPerPage);
            
            // Clear both pagination containers
            paginationTop.innerHTML = '';
            paginationBottom.innerHTML = '';
            
            if (totalPages <= 1) return;
            
            // Function to build pagination controls
            function buildPaginationControls() {{
                const controls = document.createElement('div');
                controls.style.display = 'contents';
                
                const prevBtn = document.createElement('button');
                prevBtn.className = 'pagination-btn';
                prevBtn.textContent = '‹ Назад';
                prevBtn.disabled = currentPage === 1;
                prevBtn.onclick = () => goToPage(currentPage - 1);
                controls.appendChild(prevBtn);
                
                let startPage = Math.max(1, currentPage - 3);
                let endPage = Math.min(totalPages, startPage + 6);
                
                if (endPage - startPage < 6) {{
                    startPage = Math.max(1, endPage - 6);
                }}
                
                if (startPage > 1) {{
                    const firstBtn = document.createElement('button');
                    firstBtn.className = 'pagination-btn';
                    firstBtn.textContent = '1';
                    firstBtn.onclick = () => goToPage(1);
                    controls.appendChild(firstBtn);
                    
                    if (startPage > 2) {{
                        const dots = document.createElement('span');
                        dots.className = 'pagination-info';
                        dots.textContent = '...';
                        controls.appendChild(dots);
                    }}
                }}
                
                for (let i = startPage; i <= endPage; i++) {{
                    const pageBtn = document.createElement('button');
                    pageBtn.className = 'pagination-btn' + (i === currentPage ? ' active' : '');
                    pageBtn.textContent = i;
                    pageBtn.onclick = () => goToPage(i);
                    controls.appendChild(pageBtn);
                }}
                
                if (endPage < totalPages) {{
                    if (endPage < totalPages - 1) {{
                        const dots = document.createElement('span');
                        dots.className = 'pagination-info';
                        dots.textContent = '...';
                        controls.appendChild(dots);
                    }}
                    
                    const lastBtn = document.createElement('button');
                    lastBtn.className = 'pagination-btn';
                    lastBtn.textContent = totalPages;
                    lastBtn.onclick = () => goToPage(totalPages);
                    controls.appendChild(lastBtn);
                }}
                
                const nextBtn = document.createElement('button');
                nextBtn.className = 'pagination-btn';
                nextBtn.textContent = 'Напред ›';
                nextBtn.disabled = currentPage === totalPages;
                nextBtn.onclick = () => goToPage(currentPage + 1);
                controls.appendChild(nextBtn);
                
                return controls;
            }}
            
            // Render to both top and bottom
            const topControls = buildPaginationControls();
            const bottomControls = buildPaginationControls();
            
            // Append children from the controls to the pagination containers
            while (topControls.firstChild) {{
                paginationTop.appendChild(topControls.firstChild);
            }}
            while (bottomControls.firstChild) {{
                paginationBottom.appendChild(bottomControls.firstChild);
            }}
        }}
        
        function goToPage(page) {{
            currentPage = page;
            renderTable();
            renderPagination();
            updateResultsInfo();
        }}
        
        function updateResultsInfo() {{
            const info = document.getElementById('results-info');
            const start = (currentPage - 1) * recordsPerPage + 1;
            const end = Math.min(start + recordsPerPage - 1, filteredData.length);
            const total = filteredData.length;
            
            if (total === 0) {{
                info.innerHTML = 'Няма намерени записи';
            }} else {{
                info.innerHTML = `Показани записи <strong>${{start}}-${{end}}</strong> от общо <strong>${{total}}</strong>`;
            }}
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        document.getElementById('filter-search').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                applyFilters();
            }}
        }});
    </script>
</body>
</html>'''
    
    # Write to file
    with open(f"{OUTPUT_DIR}/hunt-marks.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def main():
    print("🚀 Building modern website with modals...")
    
    # Check for required hero images first
    if not os.path.exists("hunting_hero_images") or len(os.listdir("hunting_hero_images")) == 0:
        print("❌ ERROR: No hunting hero images found!")
        print("   Please run: ./download_hunting_images.sh")
        import sys
        sys.exit(1)
    
    # Load JSON
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pages = data.get('pages', [])
    print(f"📄 Found {len(pages)} pages")
    
    # Setup
    clean_directories()
    copy_assets()
    create_modern_css()
    create_js()
    
    # Categorize pages
    categories = categorize_pages(pages)
    
    # Generate index
    print("✍ Generating homepage (3 items per section)...")
    with open(f"{OUTPUT_DIR}/index.html", 'w', encoding='utf-8') as f:
        f.write(generate_index_page(categories))
    
    # Generate listing pages
    print("✍ Generating listing pages...")
    with open(f"{OUTPUT_DIR}/hotels.html", 'w', encoding='utf-8') as f:
        f.write(generate_listing_page(
            categories['hotels'], 
            'Настаняване',
            'Комфортни ловни хижи в сърцето на природата',
            'Хижа',
            'hunting-lodge.jpg'
        ))
    
    with open(f"{OUTPUT_DIR}/services.html", 'w', encoding='utf-8') as f:
        f.write(generate_listing_page(
            categories['services'],
            'Ловни услуги',
            'Професионални ловни програми и услуги',
            'Услуга',
            'wild-deer.jpg'
        ))
    
    with open(f"{OUTPUT_DIR}/news.html", 'w', encoding='utf-8') as f:
        f.write(generate_listing_page(
            categories['news'],
            'Новини',
            'Актуални новини от света на лова',
            'Новина',
            'autumn-forest.jpg',
            is_news=True
        ))
    
    # Generate contacts page
    print("✍ Generating contacts page...")
    with open(f"{OUTPUT_DIR}/contacts.html", 'w', encoding='utf-8') as f:
        f.write(generate_contacts_page())
    
    # Generate hunt marks page
    print("✍ Generating hunt marks page...")
    if generate_hunt_marks_page():
        print("   ✅ Hunt marks page created")
    else:
        print("   ⚠️  Hunt marks page skipped (no data)")
    
    print(f"\n✅ Modern website complete!")
    print(f"   📍 {OUTPUT_DIR}/")
    print(f"   🏨 {len(categories['hotels'])} hotels")
    print(f"   🎯 {len(categories['services'])} services")
    print(f"   📰 {len(categories['news'])} news")
    print(f"   ✨ All details open in modals")
    print(f"   📱 Fully responsive")
    print(f"   🖼️  Filtered tiny images")

if __name__ == '__main__':
    main()
