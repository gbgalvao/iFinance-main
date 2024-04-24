document.getElementById('yearForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    var selectedYear = document.getElementById('expensesYear').value;

    fetch('/fetch_data_chart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ year: selectedYear })
    })
    .then(response => response.json())
    .then(data => {
        var labels = [];
        var expensesData = [];

        data.forEach(expense => {
            labels.push(expense.month);
            expensesData.push(parseFloat(expense.total_value));
        });

        var chartData = {
            labels: labels,
            datasets: [{
                label: 'Monthly expenses',
                data: expensesData,
                borderColor: 'blue',
                borderWidth: 1
            }]
        };

        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});