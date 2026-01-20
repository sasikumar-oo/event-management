/**
 * Enquiries Data Manager
 * Handles localStorage interactions for website enquiries
 */

const EnquiriesData = {
    // Initialize data if not present
    init() {
        if (!localStorage.getItem('siteEnquiries')) {
            localStorage.setItem('siteEnquiries', JSON.stringify([]));
        }
    },

    // Get all enquiries
    getAll() {
        this.init();
        const enquiries = JSON.parse(localStorage.getItem('siteEnquiries'));
        // Sort by date descending (newest first)
        return enquiries.sort((a, b) => new Date(b.date) - new Date(a.date));
    },

    // Add a new enquiry
    add(enquiry) {
        const enquiries = this.getAll();
        const newEnquiry = {
            id: 'enq_' + Date.now(),
            date: new Date().toISOString(),
            status: 'New', // New, Read, Replied
            ...enquiry
        };
        enquiries.push(newEnquiry);
        localStorage.setItem('siteEnquiries', JSON.stringify(enquiries));
        return newEnquiry;
    },

    // Get enquiry by ID
    getById(id) {
        return this.getAll().find(e => e.id === id);
    },

    // Update status (e.g. mark as read)
    updateStatus(id, status) {
        const enquiries = this.getAll();
        const index = enquiries.findIndex(e => e.id === id);
        if (index >= 0) {
            enquiries[index].status = status;
            localStorage.setItem('siteEnquiries', JSON.stringify(enquiries));
        }
    },

    // Delete an enquiry
    delete(id) {
        let enquiries = this.getAll();
        enquiries = enquiries.filter(e => e.id !== id);
        localStorage.setItem('siteEnquiries', JSON.stringify(enquiries));
    }
};

// Expose to window
window.EnquiriesData = EnquiriesData;
