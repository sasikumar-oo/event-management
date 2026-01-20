document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(n => n.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
    }));

    // Booking Form Handling
    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Simulate form submission
            const successMsg = document.getElementById('booking-success');
            successMsg.style.display = 'block';
            bookingForm.reset();
            setTimeout(() => {
                successMsg.style.display = 'none';
            }, 5000);
        });
    }

    // Contact Form Handling
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Simulate form submission
            const successMsg = document.getElementById('contact-success');
            successMsg.style.display = 'block';
            contactForm.reset();
            setTimeout(() => {
                successMsg.style.display = 'none';
            }, 5000);
        });
    }
});
