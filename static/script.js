document.addEventListener('DOMContentLoaded', function () {
    const inputImage = document.getElementById('input-image');
    const messageInput = document.getElementById('message');
    const saveBtn = document.getElementById('save-btn');
    const decodeInput = document.getElementById('decode-input');
    const decodeBtn = document.getElementById('decode-btn');
    const decodedMessage = document.getElementById('decoded-message');

    let encodedImageData = null;

    // Encode
    messageInput.addEventListener('input', () => {
        if (inputImage.files.length > 0) {
            const formData = new FormData();
            formData.append('image', inputImage.files[0]);
            formData.append('message', messageInput.value);

            fetch('/encode', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                encodedImageData = data.encoded_image;
                saveBtn.href = 'data:image/png;base64,' + encodedImageData;
            })
            .catch(error => {
                console.error('Error encoding:', error);
            });
        }
    });

    // Decode
    decodeBtn.addEventListener('click', () => {
        if (decodeInput.files.length > 0) {
            const formData = new FormData();
            formData.append('image', decodeInput.files[0]);

            fetch('/decode', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                decodedMessage.textContent = data.message;
            })
            .catch(error => {
                console.error('Error decoding:', error);
                decodedMessage.textContent = "Failed to decode message.";
            });
        } else {
            decodedMessage.textContent = "Please upload an image to decode.";
        }
    });
});
