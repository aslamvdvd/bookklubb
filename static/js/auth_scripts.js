document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.getElementById('signup_password');
    const criteriaList = document.getElementById('password-criteria-list');
    
    if (passwordField && criteriaList) {
        const criteria = {
            length: document.getElementById('length-criterion'),
            number: document.getElementById('number-criterion'),
            uppercase: document.getElementById('uppercase-criterion'),
            lowercase: document.getElementById('lowercase-criterion'),
        };

        passwordField.addEventListener('focus', function () {
            criteriaList.style.display = 'block'; /* Show on focus */
        });

        passwordField.addEventListener('input', function () {
            const value = passwordField.value;
            
            // Make sure criteria list is visible when user starts typing
            if (criteriaList.style.display === 'none') {
                 criteriaList.style.display = 'block';
            }

            // Length criterion (at least 8 characters)
            if (value.length >= 8) {
                criteria.length.classList.remove('invalid');
                criteria.length.classList.add('valid');
            } else {
                criteria.length.classList.remove('valid');
                criteria.length.classList.add('invalid');
            }

            // Number criterion
            if (/[0-9]/.test(value)) {
                criteria.number.classList.remove('invalid');
                criteria.number.classList.add('valid');
            } else {
                criteria.number.classList.remove('valid');
                criteria.number.classList.add('invalid');
            }

            // Uppercase criterion
            if (/[A-Z]/.test(value)) {
                criteria.uppercase.classList.remove('invalid');
                criteria.uppercase.classList.add('valid');
            } else {
                criteria.uppercase.classList.remove('valid');
                criteria.uppercase.classList.add('invalid');
            }

            // Lowercase criterion
            if (/[a-z]/.test(value)) {
                criteria.lowercase.classList.remove('invalid');
                criteria.lowercase.classList.add('valid');
            } else {
                criteria.lowercase.classList.remove('valid');
                criteria.lowercase.classList.add('invalid');
            }
        });
    }
}); 