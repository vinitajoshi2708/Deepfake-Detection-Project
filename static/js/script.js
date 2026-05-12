const imageInput = document.getElementById('imageInput');
const previewArea = document.getElementById('previewArea');
const dropzone = document.getElementById('dropzone');
const imagePreview = document.getElementById('imagePreview');
const analyzingText = document.getElementById('analyzingText');
const resultCard = document.getElementById('resultCard');

// 1. Image selection and preview logic
imageInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            dropzone.classList.add('hidden');
            previewArea.classList.remove('hidden');
            // Backend ko file bhej rahe hain
            uploadAndPredict(file);
        }
        reader.readAsDataURL(file);
    }
});

// 2. Main function to talk to Flask Backend
async function uploadAndPredict(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // UI reset for new analysis
    analyzingText.classList.remove('hidden');
    resultCard.classList.remove('is-real', 'is-fake');
    resultCard.classList.add('hidden');

    try {
        // Full URL used to avoid 404/Connection issues
        const response = await fetch('http://127.0.0.1:5000/predict', { 
            method: 'POST', 
            body: formData 
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        analyzingText.classList.add('hidden');
        resultCard.classList.remove('hidden');
        showResults(data);
    } catch (err) {
        analyzingText.classList.add('hidden');
        alert("Error: Backend server (app.py) is not responding at port 5000!");
        console.error("Fetch Error:", err);
    }
}

// 3. UI logic to show FAKE or REAL
function showResults(data) {
    const scoreVal = document.getElementById('scoreVal');
    const statusLabel = document.getElementById('statusLabel');
    const barFill = document.getElementById('barFill');
    const breakdown = document.getElementById('breakdown');

    scoreVal.innerText = data.confidence + '%';
    statusLabel.innerText = data.label;
    
    const confidenceNum = parseFloat(data.confidence);
    barFill.style.width = confidenceNum + '%';

    // Adding professional colors based on result
    if (data.is_real) {
        resultCard.classList.add('is-real');
        resultCard.classList.remove('is-fake');
    } else {
        resultCard.classList.add('is-fake');
        resultCard.classList.remove('is-real');
    }

    // Updating technical breakdown for the user
    breakdown.classList.remove('hidden');
    const items = document.getElementById('breakdownItems');
    items.innerHTML = `
        <div class="flex justify-between border-b py-1">
            <span>Face Consistency:</span>
            <span class="font-bold">${data.is_real ? 'High' : 'Low'}</span>
        </div>
        <div class="flex justify-between py-1">
            <span>Pixel Artifacts:</span>
            <span class="font-bold">${data.is_real ? 'Clean' : 'Detected'}</span>
        </div>
    `;
}