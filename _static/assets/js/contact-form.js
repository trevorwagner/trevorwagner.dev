const clearNotices = function () {
    document.getElementById('notices').innerHTML = '';
}


const buildErrorMessage = function (errors) {
    const errorMessage = document.createElement('div');
    errorMessage.classList.add('notice');
    errorMessage.classList.add('error');
    errorMessage.innerHTML += '<p>Unable to submit form due to issues:</p>\n';

    if (errors.length > 0) {
        errorMessage.innerHTML += `<ul>\n\t<li>${errors.join('</li>\n\t<li>')}</li>\n</ul>`;
    }

    return errorMessage;
}

const buildInput = function (config) {
    const div = document.createElement('div');

    if (config['label']) {
        const newLabel = document.createElement('label');
        newLabel.innerText = config['label'];
        div.appendChild(newLabel);
    }

    let newInput;
    if (config["type"] === "textarea") {
        newInput = document.createElement('textarea');
    } else {
        newInput = document.createElement('input');
        newInput.setAttribute('type', config['type']);
    }

    if (config["inputName"]) {
        newInput.setAttribute('name', config['inputName']);
    }

    if (config["class"]) {
        div.classList.add(config["class"]);
    }

    if (config["value"]) {
        newInput.setAttribute('value', config['value']);
    }
    div.appendChild(newInput)
    return div;
}


const buildContactForm = function () {
    const wrapper = document.createElement('div');
    wrapper.classList.add('wrapper');

    [
        { "label": "Name", "type": "text", "inputName": "name" },
        { "label": "Phone", "type": "text", "inputName": "phone", "class": "lowvis" },
        { "label": "Email", "type": "text", "inputName": "email" },
        { "label": "Message", "type": "textarea", "inputName": "message" },
    ].forEach(function (item) {
        wrapper.appendChild(buildInput(item));
    });

    wrapper.innerHTML += "\n<div><p>By submitting this form you agree to "
        + "our <a href=\"/privacy-policy/\">Privacy Policy</a>.</p></div>\n";

    wrapper.appendChild(buildInput({ "type": "submit", "value": "Submit" }));
    
    const cleardiv = document.createElement('div');
    cleardiv.setAttribute('class', 'clear-both');
    wrapper.appendChild(cleardiv);

    return wrapper;
}


const emailIsValid = function (address) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(address);
}


const handleFormSubmission = function () {
    clearNotices();

    const { formIsValid, errors } = validateForm(document.forms['contact-form']);

    if (!formIsValid) {
        displayErrorMesage(buildErrorMessage(errors))
    }

    return formIsValid;
}


const displayErrorMesage = function (message) {
    const notices = document.getElementById('notices');
    notices.appendChild(message);
}


const validateForm = function (formData) {
    let formIsValid = false;
    let errors = [];

    const fname = formData["name"].value;
    const femail = formData["email"].value;
    const fphone = formData["phone"].value;
    const fmessage = formData["message"].value;

    if (fname.length === 0) {
        errors.push('Name field is empty.');
    }

    if (fphone.length !== 0) {
        errors.push('Phone is invalid.')
    }

    if (femail.length === 0) {
        errors.push('Email field is empty.');
    } else if (!emailIsValid(femail)) {
        errors.push('Email is invalid.')
    }

    if (fmessage.length === 0) {
        errors.push('Message field is empty.');
    }

    if (errors.length === 0) {
        formIsValid = true;
    }

    return { formIsValid, errors };
}