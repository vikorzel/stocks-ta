// Stock Chart JavaScript Functions

// Submit button wrapper function
function handleSubmit(event) {
    event.preventDefault(); // Prevent default form submission
    
    const stockInput = document.getElementById('stockInput');
    const typeInput = document.getElementById('typeInput');
    
    const stockSymbol = stockInput.value.trim();
    const transactionType = typeInput.value;
    
    // Basic validation
    if (!stockSymbol) {
        alert('Please enter a stock symbol');
        return;
    }
    
    if (!transactionType) {
        alert('Please select a transaction type');
        return;
    }
    
    // Log the form data (you can replace this with actual form submission logic)
    console.log('Form submitted:', {
        stock: stockSymbol,
        type: transactionType
    });
    
    // Here you can add logic to submit the form data to your backend
    // For example: submitFormData(stockSymbol, transactionType);
    
    // Redirect to the /chart route with parameters
    window.location.href = `/chart?stock=${encodeURIComponent(stockSymbol)}&type=${encodeURIComponent(transactionType)}`;
}

// Initialize form handlers when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.input-form');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
});
