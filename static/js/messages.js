document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.querySelector('.django-messages');
    if (messagesContainer) {
        // Select only visible .alert elements within .django-messages
        // (Our CSS now ensures only errors and warnings are visible by default)
        const visibleAlerts = messagesContainer.querySelectorAll('.alert[style*="display: block"], .alert.alert-danger, .alert.alert-warning');
        // A more robust selector might be needed if display:block is not consistently set by the new CSS for all cases, 
        // but this should catch those explicitly set to display:block or having the error/warning classes.
        // However, since CSS now hides others, we can simply iterate all alerts and the timeout will only affect those not display:none.
        // Let's revert to iterating all alerts, and the timeout is for those that are visible (errors/warnings).

        const alerts = messagesContainer.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            // Check if the alert is actually visible before setting a timeout
            // GetComputedStyle can be expensive if there are many alerts, but it's reliable.
            const style = window.getComputedStyle(alert);
            if (style.display === 'none') {
                return; // Skip hidden alerts
            }

            // Apply the timeout and fade-out behavior only to visible alerts (errors/warnings)
            setTimeout(function() {
                alert.classList.add('fade-out');
                alert.addEventListener('transitionend', function() {
                    alert.remove();
                    if (messagesContainer.children.length === 0) {
                        messagesContainer.style.display = 'none';
                    }
                });
            }, 5000); // Start fade out after 5 seconds
        });
    }
}); 