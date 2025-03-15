document.addEventListener('DOMContentLoaded', () => {
  console.log("Gate animation script loaded");

  const leftPanel = document.querySelector('.gate-panel.left');
  const rightPanel = document.querySelector('.gate-panel.right');
  const gate = document.querySelector('.gate');
  const approvedContainer = document.querySelector('.approved-container');
  const vehicleNumber = document.querySelector('.vehicle-number'); // Get vehicle number element

  if (!leftPanel || !rightPanel || !gate || !approvedContainer || !vehicleNumber) {
      console.error("One or more elements not found!");
      return;
  }

  console.log("Gates found, triggering animation...");

  // Delayed start for smooth transition
  setTimeout(() => {
      leftPanel.style.transform = 'perspective(1000px) rotateY(-95deg)';
      rightPanel.style.transform = 'perspective(1000px) rotateY(95deg)';
  }, 700); // Slight delay for effect

  // Hide the gate and show the approved message after animation completes
  setTimeout(() => {
      console.log("Hiding gate, showing approved message");
      gate.style.display = 'none';
      approvedContainer.classList.add('show');

      // Set the vehicle number (you can replace this with dynamic data)
      vehicleNumber.textContent = "Vehicle #" + vehicle;// Change this to any vehicle number
  }, 7500); // Matches slower animation
});
