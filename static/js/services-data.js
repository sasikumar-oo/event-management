/**
 * Services Data Manager
 * Handles localStorage interactions for website services
 */

const DEFAULT_SERVICES = [];

const ServicesData = {
    // Initialize data if not active
    init() {
        if (!localStorage.getItem('siteServices')) {
            localStorage.setItem('siteServices', JSON.stringify(DEFAULT_SERVICES));
        }
    },

    // Get all services
    getAll() {
        this.init();
        const services = JSON.parse(localStorage.getItem('siteServices'));
        return services.sort((a, b) => a.order - b.order);
    },

    // Get only active services
    getActive() {
        return this.getAll().filter(s => s.active);
    },

    // Get services by ID
    getById(id) {
        return this.getAll().find(s => s.id === id);
    },

    // Save a service (Add or Update)
    async save(service) {
        try {
            const response = await fetch('/api/services', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(service)
            });
            const result = await response.json();
            if (result.status === 'success') {
                service.id = result.id;
            }
        } catch (e) {
            console.error("Failed to save service to server:", e);
        }

        const services = this.getAll();
        const index = services.findIndex(s => s.id == service.id || s.id == service._orig_id);

        if (index >= 0) {
            services[index] = service;
        } else {
            services.push(service);
        }

        localStorage.setItem('siteServices', JSON.stringify(services));
        return service;
    },

    // Delete a service
    async delete(id) {
        try {
            await fetch(`/api/services/${id}`, { method: 'DELETE' });
        } catch (e) {
            console.error("Failed to delete service on server:", e);
        }
        let services = this.getAll();
        services = services.filter(s => s.id != id);
        localStorage.setItem('siteServices', JSON.stringify(services));
    }
};

// Expose to window for global access
window.ServicesData = ServicesData;
