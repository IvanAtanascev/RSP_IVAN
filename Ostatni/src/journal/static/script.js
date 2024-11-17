const hamburgerMenu = document.getElementById("hamburgerMenu");
const navMenu = document.getElementById("navMenu");

hamburgerMenu.addEventListener("click", () => {
  navMenu.classList.toggle("active");
  hamburgerMenu.classList.toggle("open");
});

document.addEventListener("DOMContentLoaded", function () {
  // Select all toggle buttons
  const toggleButtons = document.querySelectorAll(".toggleHistoryButton");

  // Loop through each button and add a click event listener
  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Find the sibling history container for this button
      const historyContainer = this.nextElementSibling;

      if (historyContainer.classList.contains("hidden")) {
        historyContainer.classList.remove("hidden");
        historyContainer.classList.add("visible");
        this.textContent = "Skrýt historii"; // Update button text
      } else {
        historyContainer.classList.remove("visible");
        historyContainer.classList.add("hidden");
        this.textContent = "Ukázat historii"; // Reset button text
      }
    });
  });
});
