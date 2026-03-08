// script.js

document.addEventListener('DOMContentLoaded', () => {

    // 1. Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const closeMenu = document.querySelector('.close-menu');
    const mobileLinks = document.querySelectorAll('.mobile-nav-links a');

    if (hamburger && mobileMenu && closeMenu) {
        hamburger.addEventListener('click', () => {
            mobileMenu.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        closeMenu.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = 'auto';
        });

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        });
    }

    // 2. Navbar Scroll Effect
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 3. Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal-up');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 100;

        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;

            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);

    // Initial trigger to reveal elements visible on load
    setTimeout(revealOnScroll, 300);

    // 4. Update Footer Year Auto
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // 5. Booking Form Submission handling (Real API Request)
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = bookingForm.querySelector('button');
            const originalText = btn.textContent;

            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
            btn.style.opacity = '0.8';
            btn.style.pointerEvents = 'none';

            // Collect data
            const inputs = bookingForm.querySelectorAll('input, select, textarea');
            const data = {
                name: inputs[0].value,
                email: inputs[1].value,
                phone: inputs[2].value,
                service: inputs[3].value,
                message: inputs[4].value
            };

            try {
                // Real API Request to Flask Backend
                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    btn.style.background = '#28a745';
                    btn.innerHTML = '<i class="fa-solid fa-check"></i> ' + result.message;

                    setTimeout(() => {
                        bookingForm.reset();
                        btn.style.background = '';
                        btn.textContent = originalText;
                        btn.style.opacity = '1';
                        btn.style.pointerEvents = 'all';
                    }, 3000);
                }
            } catch (error) {
                btn.style.background = '#dc3545';
                btn.innerHTML = '<i class="fa-solid fa-xmark"></i> Error sending request';

                setTimeout(() => {
                    btn.style.background = '';
                    btn.textContent = originalText;
                    btn.style.opacity = '1';
                    btn.style.pointerEvents = 'all';
                }, 3000);
            }
        });
    }

    // 6. Gallery Filtering
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            galleryItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.classList.remove('hide');
                    // Re-trigger reveal animation implicitly
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                        item.style.display = 'block';
                    }, 50);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.classList.add('hide');
                    }, 300); // Wait for transition before hiding
                }
            });

            // Re-trigger scroll reveal after filtering to fix spaces
            setTimeout(revealOnScroll, 350);
        });
    });

    // 7. FAQ Accordion Logic
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;

            // Smoothly close previously opened accordions (Optional, but elegant)
            accordionHeaders.forEach(otherHeader => {
                if (otherHeader !== header && otherHeader.classList.contains('active')) {
                    otherHeader.classList.remove('active');
                    otherHeader.nextElementSibling.style.maxHeight = null;
                }
            });

            // Toggle current
            header.classList.toggle('active');

            if (header.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.style.maxHeight = null;
            }
        });
    });

    // 8. Active Link Highlighting
    const currentPath = window.location.pathname.split('/').pop();
    const navLinksList = document.querySelectorAll('.nav-links a');

    // Default highlight Home if root or empty
    if (!currentPath || currentPath === '') {
        navLinksList.forEach(link => {
            if (link.getAttribute('href') === 'index.html' || link.getAttribute('href') === '#home') {
                link.classList.add('active');
            }
        });
    } else {
        navLinksList.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    // 9. Auto-select Contact Form Options based on URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const selectedPackage = urlParams.get('package');
    const formSelect = document.querySelector('#bookingForm select');

    if (selectedPackage && formSelect) {
        // Find matching option or default to "other" if Custom Elite
        let optionFound = false;
        Array.from(formSelect.options).forEach(option => {
            if (option.value === selectedPackage || option.textContent.toLowerCase().includes(selectedPackage)) {
                option.selected = true;
                optionFound = true;
            }
        });

        // If package is elite or specific combo
        if (!optionFound) {
            formSelect.value = "other";
            const textarea = document.querySelector('#bookingForm textarea');
            if (textarea) {
                textarea.value = `I am interested in the ${selectedPackage.charAt(0).toUpperCase() + selectedPackage.slice(1)} Event Package. Please contact me with more details.`;
            }
        }
    }
});
