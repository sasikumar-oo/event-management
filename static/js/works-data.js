/**
 * Works (Portfolio) Data Manager
 * Handles localStorage interactions for "Works of Us"
 */

const DEFAULT_WORKS = [];

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
    async save(work) {
        try {
            const response = await fetch('/api/works', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(work)
            });
            const result = await response.json();
            if (result.status === 'success') {
                work.id = result.id;
            }
        } catch (e) {
            console.error("Failed to save work to server:", e);
        }

        const works = this.getAll();
        const index = works.findIndex(w => w.id == work.id);

        if (index >= 0) {
            works[index] = work;
        } else {
            works.push(work);
        }

        localStorage.setItem('siteWorks', JSON.stringify(works));
        return work;
    },

    // Delete
    async delete(id) {
        try {
            await fetch(`/api/works/${id}`, { method: 'DELETE' });
        } catch (e) {
            console.error("Failed to delete work on server:", e);
        }
        let works = this.getAll();
        works = works.filter(w => w.id != id);
        localStorage.setItem('siteWorks', JSON.stringify(works));
    }
};

window.WorksData = WorksData;
