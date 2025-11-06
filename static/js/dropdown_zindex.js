// Dropdown z-index management
document.addEventListener('DOMContentLoaded', function() {
    // Listen for all dropdown show events
    document.addEventListener('show.bs.dropdown', function(event) {
        // Find the closest card parent
        const card = event.target.closest('.card');
        if (card) {
            card.classList.add('dropdown-active-card');
            card.style.zIndex = '10000';
        }
    });

    // Listen for all dropdown hide events
    document.addEventListener('hide.bs.dropdown', function(event) {
        // Find the closest card parent
        const card = event.target.closest('.card');
        if (card) {
            card.classList.remove('dropdown-active-card');
            card.style.zIndex = '1';
        }
    });
});
