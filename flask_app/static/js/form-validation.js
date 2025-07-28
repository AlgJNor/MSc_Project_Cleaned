const form  = document.getElementById("emailForm")
const submitBtn  = document.getElementById("submitBtn")
const errorMessage  = document.getElementById("error")
const loadingSpinner  = document.getElementById("loadingSpinner")

form.addEventListener("submit", function (e) {

    const email_text = document.getElementById("emailText").value.trim()
    if(!email_text) {
        e.preventDefault();
        errorMessage.textContent = "\You must enter your email text";
        errorMessage.style.display = "block";
        return;
    }

    if(email_text > 10000) {
        e.preventDefault();
        errorMessage.textContent = "\The email text is above the limit, please enter an email below 10000 characters";
        errorMessage.style.display = "block";
        return;
    }

    //if input is valid
    submitBtn.disabled = true;
    loadingSpinner.style.display = "inline";

})