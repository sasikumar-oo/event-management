/**
 * Services Data Manager
 * Handles localStorage interactions for website services
 */

const DEFAULT_SERVICES = [
    {
        id: 'svc_1',
        title: 'Wedding Planning',
        shortDesc: 'From the proposal to the reception, we create fairy-tale weddings.',
        fullDesc: 'Our wedding planning service covers every detail, ensuring your special day is stress-free and spectacular. We handle venue selection, catering, decoration, logistics, and on-day coordination.',
        icon: 'fa-ring',
        image: 'https://images.unsplash.com/photo-1519741497674-611481863552?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        order: 1
    },
    {
        id: 'svc_2',
        title: 'Corporate Events',
        shortDesc: 'Professional event management for conferences and company galas.',
        fullDesc: 'We execute flawless corporate events that reflect your brand identity. From product launches to team building retreats, we ensure professionalism and engagement.',
        icon: 'fa-briefcase',
        image: 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        order: 2
    },
    {
        id: 'svc_3',
        title: 'Birthday Parties',
        shortDesc: 'Make your special day unforgettable with expert party planning.',
        fullDesc: 'Whether it is a milestone birthday or a kids party, we bring fun and creativity to the table with themed decorations, entertainment, and catering.',
        icon: 'fa-birthday-cake',
        image: 'https://images.unsplash.com/photo-1530103862676-de3c9a59af38?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        order: 3
    },
    {
        id: 'svc_4',
        title: 'Concerts & Shows',
        shortDesc: 'Full-scale production management for live entertainment.',
        fullDesc: 'We manage large-scale concerts and stage shows, handling sound, lighting, stage design, artist management, and crowd control.',
        icon: 'fa-music',
        image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        order: 4
    },
    {
        id: 'svc_5',
        title: 'Decoration & Catering',
        shortDesc: 'Exquisite decor styling and gourmet catering coordination.',
        fullDesc: 'Transform any space with our artistic decoration services and delight your guests with curated menus from top-tier caterers.',
        icon: 'fa-utensils',
        image: 'https://images.unsplash.com/photo-1555244162-803834f70033?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        order: 5
    }
];

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
    save(service) {
        const services = this.getAll();
        const index = services.findIndex(s => s.id === service.id);

        if (index >= 0) {
            // Update
            services[index] = service;
        } else {
            // Add new
            service.id = 'svc_' + Date.now();
            services.push(service);
        }

        localStorage.setItem('siteServices', JSON.stringify(services));
        return service;
    },

    // Delete a service
    delete(id) {
        let services = this.getAll();
        services = services.filter(s => s.id !== id);
        localStorage.setItem('siteServices', JSON.stringify(services));
    }
};

// Expose to window for global access
window.ServicesData = ServicesData;
