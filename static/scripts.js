document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(event.target);
    let formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.prediction;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred. Please try again.';
    });
});
