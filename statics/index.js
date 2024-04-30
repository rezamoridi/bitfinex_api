function updateTicker() {
  // Make a request to fetch the updated ticker value
  fetch("/ticker")
      .then(response => response.text())
      .then(data => {
          // Update the ticker value
          document.getElementById("tickerValue").innerText = data;
      })
      .catch(error => console.error('Error updating ticker:', error));
}

// Update the ticker every 5 seconds
setInterval(updateTicker, 5000);

// Initial update
updateTicker();