const form  = document.getElementById("emailForm")
const submitBtn  = document.getElementById("submitBtn")
const errorMessage  = document.getElementById("error")
const loadingSpinner  = document.getElementById("loadingSpinner")
const charCount = document.getElementById("charCount");
const emailTextArea = document.getElementById("emailText");
form.addEventListener("submit", function (e) {

    const email_text = emailTextArea.value.trim()
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

emailTextArea.addEventListener("input", () => {
    const currentLength = emailTextArea.value.length
    charCount.textContent = `Characters: ${currentLength} / 10000`

    if(currentLength > 9500 && currentLength <= 10000) {
        charCount.classList.remove("text-muted");
        charCount.classList.add("text-warning");
    }
    else if (currentLength > 10000) {
        charCount.classList.remove("text-warning");
        charCount.classList.add("text-danger");
    }
    else {
         charCount.classList.remove("text-warning", "text-danger");
        charCount.classList.add("text-muted");
    }
})