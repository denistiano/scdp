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