const form = document.getElementById('form');
const username = document.getElementById('username');
const email = document.getElementById('email');
const password = document.getElementById('password');
const cpassword = document.getElementById('cpassword');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    validateInputs(); //
});

const setError = (element, message) => {
    const fieldContainer = element.parentElement;
    const errorSpan = fieldContainer.querySelector('.error');
    errorSpan.innerHTML = 
    `   <i class="fa-solid fa-circle-exclamation error-icon"></i>
        <p>${message}</p>
    `;

    fieldContainer.classList.add('error');
    fieldContainer.classList.remove('success')
};

const setSuccess = element => {
    const fieldContainer = element.parentElement;
    const errorSpan = fieldContainer.querySelector('.error');

    errorSpan.innerHTML = '';
    fieldContainer.classList.add('success');
    fieldContainer.classList.remove('error');
};

const isValidEmail = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
};

const validateUsername = () => {
    const usernameValue = username.value.trim();

    if (usernameValue === '') {
        setError(username, 'Username is required.');
    } else {
        setSuccess(username);
    }
}

const validateEmail = () => {    
    const emailValue = email.value.trim();

    if (emailValue === '') {
        setError(email, 'Email is required.');
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Please provide a valid email address.');
    } else {
        setSuccess(email);
    }
}

const validatePassword = () => {
    const passwordValue = password.value.trim();

    if (passwordValue === '') {
        setError(password, 'Password is required.');
    } else if (passwordValue.length < 8 ) {
        setError(password, 'Password must be at least 8 characters.')
    } else {
        setSuccess(password);
    }
}

const validateConfirmPassword = () => {
    const passwordValue = password.value.trim();
    const cpasswordValue = cpassword.value.trim();

    if (cpasswordValue === '') {
        setError(cpassword, 'Confirm password is required.');
    } else if (cpasswordValue !== passwordValue) {
        setError(cpassword, "Passwords don't match.");
    } else {
        setSuccess(cpassword);
    }
}

const validateInputs = () => {
    validateUsername();
    validateEmail();
    validatePassword();
    validateConfirmPassword();
};

username.addEventListener('focusout', validateUsername);
email.addEventListener('focusout', validateEmail);
password.addEventListener('focusout', validatePassword);
cpassword.addEventListener('focusout', validateConfirmPassword);