document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Check if fields are empty
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    if (!username) {
        displayErrorMessage("Please enter a username");
    } else if (!password) {
        displayErrorMessage("Please enter a password");
    } else {
        sendLogin();
    }
    
    // Rest of your form handling logic here
    function sendLogin() {
        var form = document.getElementById('loginForm');  
        var formData = new FormData(form);
        var serializedData = {};

        for (var [key, value] of formData.entries()) {
            serializedData[key] = value;
        }

        // Send post request
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(serializedData),
        })
        .then(response => {
            if (response.status === 403) {
                // Handle 403 forbidden error
                displayErrorMessage("Incorrect username or password");
            } else if (response.ok) {
                // Handle if ok
                window.location.href = '/';
            } else {
                // Handle other errors
                displayErrorMessage("An error occurred. Please try again later.");
            }
        })
        .catch(error => {
            // Handle network errors or other exceptions
            displayErrorMessage("An error occurred. Please check your network connection.");
            console.error('Error:', error);
        });
            
    }
});


function displayErrorMessage(message) {
    // Display error message on the screen (e.g., in a <div> with id "error-message")
    var errorMessageElement = document.getElementById('error-message');
    if (errorMessageElement) {
        errorMessageElement.innerHTML = `<p>${message}</p>`;
    }
}

function clearErrorMessage() {
    var errorMessageElement = document.getElementById('error-message');
    if (errorMessageElement) {
        errorMessageElement.innerHTML = ''; // Clear the error message
    }
}