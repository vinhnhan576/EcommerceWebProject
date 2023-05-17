const form = document.getElementById('form');
const username = document.getElementById('username');
const password = document.getElementById('password');
const cpassword = document.getElementById('cpassword');
const address = document.getElementById('address');
const phone = document.getElementById('phone');

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
    fieldContainer.classList.remove('success')
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

const validateConfirmPassword = () => {
    const passwordValue = password.value.trim();
    const cpasswordValue = cpassword.value.trim();

    if (cpasswordValue === '') {
        setError(cpassword, 'Confirm password is required.');
        return false;
    } else if (cpasswordValue !== passwordValue) {
        setError(cpassword, "Passwords don't match.");
        return false;
    } else {
        setSuccess(cpassword);
        return true;
    }
};

const validateAddress = () => {
    const addressValue = address.value.trim();

    if (addressValue === '') {
        setError(address, 'Address is required.');
        return false;
    } else {
        setSuccess(address);
        return true;
    }
};

const isValidPhone = (phoneNumber) => {
    const re = /^(0|\+84)(\d{9})$/;
    return re.test(phoneNumber);
}

const validatePhone = () => {
    const phoneValue = phone.value.trim();

    if (phoneValue === '') {
        setError(phone, 'Phone is required.');
        return false;
    } else if (!isValidPhone(phoneValue)) {
        setError(phone, 'Please provide a valid phone number.')
        return false;
    } else {
        setSuccess(phone);
        return true;
    }
}

const validateInputs = () => {
    return validateUsername() && validatePassword() && validateConfirmPassword() && validateAddress() && validatePhone();
};

username.addEventListener('focusout', validateUsername);
password.addEventListener('focusout', validatePassword);
cpassword.addEventListener('focusout', validateConfirmPassword);
address.addEventListener('focusout', validateAddress);
phone.addEventListener('focusout', validatePhone);