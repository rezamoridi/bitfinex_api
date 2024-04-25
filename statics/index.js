// Get the input and the datalist
var input = document.getElementById('symbol');
var datalist = document.getElementById('symbols');

// Add an event listener for when the input value changes
input.addEventListener('input', function() {
  // Get the input value
  var inputValue = input.value;

  // Loop through the options in the datalist
  var options = datalist.getElementsByTagName('option');
  var matchFound = false;
  for (var i = 0; i < options.length; i++) {
    // Check if the input value matches any of the options
    if (inputValue === options[i].value) {
      matchFound = true;
      break;
    }
  }

  // If no match is found, clear the input
  if (!matchFound) {
    input.setCustomValidity("Please select a valid option from the list.");
  } else {
    input.setCustomValidity(""); // Reset validation message
  }
});