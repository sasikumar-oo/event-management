/**
 * Works (Portfolio) Data Manager
 * Handles localStorage interactions for "Works of Us"
 */

const DEFAULT_WORKS = [
    {
        id: 'work_1',
        title: 'Golden Wedding',
        category: 'Wedding',
        location: 'Grand Hotel',
        description: 'A luxurious wedding ceremony attended by 500 guests with full floral decor and live orchestra.',
        image: 'https://images.unsplash.com/photo-1519741497674-611481863552?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        date: '2025-10-15'
    },
    {
        id: 'work_2',
        title: 'Tech Summit 2025',
        category: 'Corporate',
        location: 'Convention Center',
        description: 'International technology conference hosting 500+ delegates with keynote stages and networking zones.',
        image: 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        date: '2025-11-20'
    },
    {
        id: 'work_3',
        title: 'Summer Gala',
        category: 'Social Party',
        location: 'City Gardens',
        description: 'An enchanting evening of music, dining, and charity fundraising under the stars.',
        image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        active: true,
        date: '2025-07-10'
    }
];

const WorksData = {
    // Initialize data if not present
    init() {
        if (!localStorage.getItem('siteWorks')) {
            localStorage.setItem('siteWorks', JSON.stringify(DEFAULT_WORKS));
        }
    },

    // Get all works
    getAll() {
        this.init();
        return JSON.parse(localStorage.getItem('siteWorks'));
    },

    // Get active works
    getActive() {
        return this.getAll().filter(w => w.active);
    },

    // Get by ID
    getById(id) {
        return this.getAll().find(w => w.id === id);
    },

    // Save (Add/Update)
    save(work) {
        const works = this.getAll();
        const index = works.findIndex(w => w.id === work.id);

        if (index >= 0) {
            works[index] = work;
        } else {
            work.id = 'work_' + Date.now();
            works.push(work);
        }

        localStorage.setItem('siteWorks', JSON.stringify(works));
        return work;
    },

    // Delete
    delete(id) {
        let works = this.getAll();
        works = works.filter(w => w.id !== id);
        localStorage.setItem('siteWorks', JSON.stringify(works));
    }
};

window.WorksData = WorksData;
