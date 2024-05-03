// scripts.js

// Function to submit the form when the select element's value changes
function submitFormOnChange(selectElementId) {
   var selectElement = document.getElementById(selectElementId);
   if (selectElement) {
       selectElement.addEventListener('change', function() {
           this.form.submit();
       });
   }
}
