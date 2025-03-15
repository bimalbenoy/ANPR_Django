document.addEventListener('DOMContentLoaded', () => {
    console.log("Gate closing script loaded");

    const leftPanel = document.querySelector('.gate-panel.left');
    const rightPanel = document.querySelector('.gate-panel.right');
    const gate = document.querySelector('.gate');
    const declinedContainer = document.querySelector('.declined-container');

    if (!leftPanel || !rightPanel || !gate || !declinedContainer) {
        console.error("One or more elements not found!");
        return;
    }

    console.log("Gates found, triggering closing animation...");

    // Start with gates open
    leftPanel.style.transform = 'perspective(1000px) rotateY(-90deg)';
    rightPanel.style.transform = 'perspective(1000px) rotateY(90deg)';

    // Close the gates after a short delay
    setTimeout(() => {
        leftPanel.style.transform = 'perspective(1000px) rotateY(0deg)';
        rightPanel.style.transform = 'perspective(1000px) rotateY(0deg)';
    }, 500); // Delay to ensure smooth transition start

    // Show declined message after gates are fully closed
    setTimeout(() => {
        console.log("Showing declined message");
        declinedContainer.classList.add('show');
    }, 6500); // Matches closing animation duration
});
