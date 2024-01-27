function changeContent(newContent) {
    var paragraphElement = document.querySelector('#customAlertModal .modal-body p');
    if (paragraphElement) {
        paragraphElement.textContent = newContent;
    }
}

function waitTime(seconds, callback) {
        setTimeout(callback, seconds * 1000);
    }
    
function login_portal() {
    var sendButton = document.getElementById("codeButton");
    if (sendButton.style.display == 'block') {
        $('#customAlertModal').modal('show');
        var codeValue = document.querySelector('input[type="text"]').value;
        fetch('/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers as needed
            },
            body: JSON.stringify({
                code: codeValue,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // assuming response is in JSON format
        })
            .then(data => {
                $('#customAlertModal').modal('hide');
                // Wait for a short delay (e.g., 500 milliseconds) before showing the modal and changing content
                waitTime(0.5, function() {
                    // Show the modal
                    alert("Completed creating schedule!")                
                });
        })
        .catch(error => {
            // Handle errors here
            console.error("Login failed:", error.message);
            // Display error message to the user
        });
    }
    else {
        console.log("Sign in button clicked!");

        var emailValue = document.querySelector('input[type="email"]').value;
        var passwordValue = document.querySelector('input[type="password"]').value;

        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add any other headers as needed
            },
            body: JSON.stringify({
                email: emailValue,
                password: passwordValue,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // assuming response is in JSON format
        })
        .then(data => {
            // Handle successful login here
            if (data['status'] == 'failLogin') {
                alert("Your account or password is incorrect. Please try again!");
            }
            else if (data['status'] == 'successSendCode') {
                var signInButton = document.getElementById("signInButton");
                signInButton.style.display = 'none';
                var codeField = document.getElementById("codeField");
                codeField.style.display = 'block';
                var codeButton = document.getElementById("codeButton");
                codeButton.style.display = 'block';
            }
        })
        .catch(error => {
            // Handle errors here
            console.error("Login failed:", error.message);
            // Display error message to the user
        });
    }
}
