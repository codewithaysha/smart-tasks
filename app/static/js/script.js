// Smart Tasks JavaScript utilities

document.addEventListener('DOMContentLoaded', function() {
    // Add any interactive features here
    console.log('Smart Tasks app loaded');
});

// Function to toggle task status
async function toggleTaskStatus(taskId) {
    try {
        const response = await fetch(`/tasks/${taskId}/toggle-status`, {
            method: 'POST'
        });
        const data = await response.json();
        location.reload();
    } catch (error) {
        console.error('Error:', error);
    }
}
