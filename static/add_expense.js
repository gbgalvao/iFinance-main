document.getElementById('addExpenseBtn').addEventListener('click', function() {
    createExpenseForm();
  });
  
function createExpenseForm() {
  // Create form elements
  var form = document.createElement('form');
  form.setAttribute('id', 'expenseForm');

  var container = document.createElement('div');
  container.classList.add('container');

  var row = document.createElement('div');
  row.classList.add('row');

  var nameCol = document.createElement('div');
  nameCol.classList.add('col-md-3');

  var nameInput = document.createElement('input');
  nameInput.setAttribute('type', 'text');
  nameInput.setAttribute('placeholder', 'Product/Service Name');
  nameInput.setAttribute('name', 'name');
  nameInput.classList.add('form-control');

  var categoryCol = document.createElement('div');
  categoryCol.classList.add('col-md-3');

  var categorySelect = document.createElement('select');
  categorySelect.setAttribute('name', 'category');
  categorySelect.classList.add('form-control');
  var optionDisabled = document.createElement('option');
  optionDisabled.setAttribute('disabled', 'true');
  optionDisabled.setAttribute('selected', 'true');
  optionDisabled.textContent = "Select a category";
  categorySelect.appendChild(optionDisabled);

  var priceCol = document.createElement('div');
  priceCol.classList.add('col-md-2');

  var priceInput = document.createElement('input');
  priceInput.setAttribute('type', 'number');
  priceInput.setAttribute('name', 'price');
  priceInput.setAttribute('placeholder', 'Price');
  priceInput.setAttribute('step', '0.01');
  priceInput.classList.add('form-control');

  var dateCol = document.createElement('div');
  dateCol.classList.add('col-md-2');

  var dateInput = document.createElement('input');
  dateInput.setAttribute('type', 'date');
  dateInput.setAttribute('name', 'date');
  dateInput.setAttribute('placeholder', 'Date');
  dateInput.classList.add('form-control');

  var submitCol = document.createElement('div');
  submitCol.classList.add('col-md-2', 'd-flex', 'align-items-end');

  var submitBtn = document.createElement('input');
  submitBtn.setAttribute('type', 'submit');
  submitBtn.setAttribute('value', 'Submit');
  submitBtn.classList.add('btn', 'btn-primary');

  // Fetch categories and populate select options
  fetch('/get_categories')
    .then(response => response.json())
    .then(data => {
      var categories = data.categories;
      
      categories.forEach(category => {
        var option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categorySelect.appendChild(option);
      });
    })
    .catch(error => {
      console.error('Error fetching categories:', error);
    });

  // Append elements to the form
  form.appendChild(container);
  container.appendChild(row);

  row.appendChild(nameCol);
  nameCol.appendChild(nameInput);

  row.appendChild(categoryCol);
  categoryCol.appendChild(categorySelect);

  row.appendChild(priceCol);
  priceCol.appendChild(priceInput);

  row.appendChild(dateCol);
  dateCol.appendChild(dateInput);

  row.appendChild(submitCol);
  submitCol.appendChild(submitBtn);

  // Append the form to the container
  var containerElement = document.getElementById('expenseFormContainer');
  containerElement.innerHTML = ''; // Clear previous content
  containerElement.appendChild(form);

  // Add event listener for form submission
  form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Serialize form data
    var formData = new FormData(form);
    var serializedData = {};
    for (var [key, value] of formData.entries()) {
      serializedData[key] = value;
    }

    // Send POST request
    fetch('/add_expense', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(serializedData),
    })
    .then(response => {
      // Handle the response here if needed
      console.log('Request sent:', response);

      window.location.href = '/';
    })
    .catch(error => {
      // Handle errors
      console.error('Error:', error);
    });
  });
}
  
  