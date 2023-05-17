const form = document.getElementById('form');
const username = document.getElementById('username');
const password = document.getElementById('password');

form.addEventListener('change', () => {
    document.getElementById('submitBtn').disabled = !validateInputs()
});

const setError = (element, message) => {
    const fieldContainer = element.parentElement;
    const errorSpan = fieldContainer.querySelector('.error');
    errorSpan.innerHTML =
        `   <i class="fa-solid fa-circle-exclamation error-icon"></i>
        <p>${message}</p>
    `;

    fieldContainer.classList.add('error');
    fieldContainer.classList.remove('success');
};

const setSuccess = element => {
    const fieldContainer = element.parentElement;
    const errorSpan = fieldContainer.querySelector('.error');

    errorSpan.innerHTML = '';
    fieldContainer.classList.add('success');
    fieldContainer.classList.remove('error');
};

const validateUsername = () => {
    const usernameValue = username.value.trim();

    if (usernameValue === '') {
        setError(username, 'Username is required.');
        return false;
    } else {
        setSuccess(username);
        return true;
    }
};

const validatePassword = () => {
    const passwordValue = password.value.trim();

    if (passwordValue === '') {
        setError(password, 'Password is required.');
        return false;
    } else if (passwordValue.length < 8 ) {
        setError(password, 'Password must be at least 8 characters.')
        return false;
    } else {
        setSuccess(password);
        return true;
    }
};

const validateInputs = () => {
    return validateUsername() && validatePassword();
};

username.addEventListener('focusout', validateUsername);
password.addEventListener('focusout', validatePassword);