document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    // Function to update icon visibility based on current theme on <html> element
    function updateIcons() {
        if (!themeToggleDarkIcon || !themeToggleLightIcon) return; // Guard clause

        if (document.documentElement.classList.contains('dark')) {
            themeToggleLightIcon.classList.remove('hidden');
            themeToggleDarkIcon.classList.add('hidden');
        } else {
            themeToggleDarkIcon.classList.remove('hidden');
            themeToggleLightIcon.classList.add('hidden');
        }
    }

    // Initial icon state update based on the theme applied by inline script
    updateIcons();

    themeToggleBtn?.addEventListener('click', () => {
        // Check the current state of the <html> element
        const isCurrentlyDark = document.documentElement.classList.contains('dark');

        if (isCurrentlyDark) {
            // Switch to light theme
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            // Switch to dark theme
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
        
        // Update icons to reflect the new theme state
        updateIcons(); 
    });
}); 