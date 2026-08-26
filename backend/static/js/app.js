/**
 * Aura Global JavaScript
 * 
 * Handles core functionality that spans across all pages.
 */
/**
 * Theme Manager
 */
const ThemeManager = {
    init: function() {
        // Run immediately to prevent flash
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        // Attach event listeners when DOM loads
        document.addEventListener('DOMContentLoaded', () => {
            this.bindToggles();
        });
    },

    toggle: function() {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        }
    },

    bindToggles: function() {
        const toggles = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile, .theme-toggle-btn');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggle();
            });
        });
    }
};

// Initialize immediately
ThemeManager.init();

document.addEventListener('DOMContentLoaded', () => {
    // Global initializations here
});
