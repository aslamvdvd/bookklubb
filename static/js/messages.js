document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.querySelector('.django-messages');
    if (messagesContainer) {
        const alerts = messagesContainer.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            setTimeout(function() {
                alert.classList.add('fade-out');
                // Remove the element after the transition is complete
                alert.addEventListener('transitionend', function() {
                    alert.remove();
                    // If all alerts are removed, hide the container itself (though it should be empty)
                    if (messagesContainer.children.length === 0) {
                        messagesContainer.style.display = 'none'; // or messagesContainer.remove();
                    }
                });
            }, 5000); // Start fade out after 5 seconds
        });
    }
}); 