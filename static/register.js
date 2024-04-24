document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Check if fields are empty
    var name = document.getElementById('name').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var confirmation = document.getElementById('confirmation').value;
    if (!name) {
        displayErrorMessage("Please enter a name");
    }
    else if (!username) {
        displayErrorMessage("Please enter a username");
    } else if (!password) {
        displayErrorMessage("Please enter a password");
    } else if (confirmation != password) {
        displayErrorMessage("Passwords must match!");
    } else {
        sendRegister();
    }
    
    // Rest of your form handling logic here
    function sendRegister() {
        var form = document.getElementById('registerForm');  
        var formData = new FormData(form);
        var serializedData = {};

        for (var [key, value] of formData.entries()) {
            serializedData[key] = value;
        }

        // Send post request
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(serializedData),
        })
        .then(response => {
            if (response.status == 400) {
                displayErrorMessage("No name provided");
            }
            else if (response.status === 406) {
                // Handle 406 forbidden error
                displayErrorMessage("Passwords must match");
            } else if (response.ok) {
                // Handle if ok
                window.location.href = '/login';
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