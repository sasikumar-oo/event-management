
/**
 * Settings Loader
 * Loads website settings from localStorage and applies them to specific DOM elements.
 * 
 * Target Elements ID guide:
 * - site-name: Website Title
 * - site-hero-headline: Hero H1
 * - site-hero-subtext: Hero P
 * - site-phone: Phone number (text)
 * - site-phone-link: Phone number (href)
 * - site-email: Email (text)
 * - site-email-link: Email (href)
 * - site-address: Office Address
 * - site-footer-text: Footer description
 * - site-map: Iframe src
 * - site-facebook, site-twitter, site-instagram: Social Links (href)
 */

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
});

function loadSettings() {
    const settings = JSON.parse(localStorage.getItem('siteSettings'));

    if (!settings) {
        // Default settings if nothing saved
        return;
    }

    // List of text content mappings
    const textMappings = {
        'site-name': settings.siteName,
        'site-hero-headline': settings.heroHeadline,
        'site-hero-subtext': settings.heroSubtext,
        'site-phone': settings.phone,
        'site-email': settings.email,
        'site-address': settings.address,
        'site-footer-text': settings.footerText
    };

    // Apply Text Content
    for (const [id, value] of Object.entries(textMappings)) {
        if (value) {
            const elements = document.querySelectorAll(`.${id}, #${id}`);
            elements.forEach(el => el.textContent = value);
        }
    }

    // Attributes
    if (settings.phone) {
        document.querySelectorAll('.site-phone-link, #site-phone-link').forEach(el => el.href = `tel:${settings.phone}`);
    }
    if (settings.email) {
        document.querySelectorAll('.site-email-link, #site-email-link').forEach(el => el.href = `mailto:${settings.email}`);
    }
    if (settings.facebook) {
        document.querySelectorAll('.site-facebook, #site-facebook').forEach(el => el.href = settings.facebook);
    }
    if (settings.instagram) {
        document.querySelectorAll('.site-instagram, #site-instagram').forEach(el => el.href = settings.instagram);
    }
    if (settings.twitter) {
        document.querySelectorAll('.site-twitter, #site-twitter').forEach(el => el.href = settings.twitter);
    }
    if (settings.mapUrl && document.getElementById('site-map')) {
        document.getElementById('site-map').src = settings.mapUrl;
    }
}
