window.tailwind = window.tailwind || {};
window.tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: '#111827', // Dark gray/black
                accent: '#F43F5E', // Rose
                brand: {
                    50: '#f5f3ff',
                    100: '#ede9fe',
                    500: '#8b5cf6',
                    600: '#7c3aed',
                    DEFAULT: '#F3F4F6'
                },
                theme: {
                    bg: {
                        base: 'var(--theme-bg-base)',
                        surface: 'var(--theme-bg-surface)',
                        elevated: 'var(--theme-bg-elevated)',
                        hover: 'var(--theme-bg-hover)',
                    },
                    text: {
                        base: 'var(--theme-text-base)',
                        muted: 'var(--theme-text-muted)',
                        inverse: 'var(--theme-text-inverse)',
                    },
                    border: {
                        base: 'var(--theme-border-base)',
                        divider: 'var(--theme-border-divider)',
                    },
                    input: {
                        bg: 'var(--theme-input-bg)',
                        border: 'var(--theme-input-border)',
                        placeholder: 'var(--theme-input-placeholder)',
                    },
                    primary: {
                        hover: 'var(--theme-primary-hover)',
                    }
                }
            },
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
            }
        }
    }
};
