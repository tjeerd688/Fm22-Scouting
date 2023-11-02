$(document).ready(function () {
    let sortOrder = 0; // Initialize sort order for "Goals" column to 0 (ascending)

    // Event delegation for clickable table headers
    $('#container').on('click', 'th', function () {
        const columnIndex = this.cellIndex;

        if (columnIndex === 2) { // Check if it's the "Goals" column
            sortTable(columnIndex, sortOrder);
            sortOrder = 1 - sortOrder; // Toggle sort order
            updateSortIndicator(this, sortOrder);
        }
    });
});

async function getUsers() {
    try {
        const response = await fetch(
            'http://127.0.0.1:8000/test',
            {
                method: 'GET',
            },
        );

        if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.log(error);
    }
}

function generateTable(data) {
    let table = '<table style="border-collapse: collapse;">';

    table += `
        <thead>
        <tr>
          <th>Naam</th>
          <th>Club</th>
          <th>Goals</th>
          <th>Xg</th>
        </tr>
        </thead>
  
        <tbody>
    `;

    Object.entries(data).map(user => {
        const goals = parseInt(user[1].Dlp);

        table += `
        <tr>
          <td>${user[1].Naam}</td>
          <td>${user[1].Club}</td>
          <td>${isNaN(goals) ? 'N/A' : goals}</td> <!-- Display 'N/A' for invalid goals -->
          <td>${user[1].xG}</td>
        </tr>
      `;
    });

    table += `
      </tbody>
    </table>
    `;

    const container = document.getElementById('container');
    container.innerHTML = table;
}

function sortTable(columnIndex, sortOrder) {
    let table, rows, switching, i, x, y, shouldSwitch;
    table = document.querySelector('#container table');
    switching = true;

    while (switching) {
        switching = false;
        rows = table.getElementsByTagName('tr');

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName('td')[columnIndex];
            y = rows[i + 1].getElementsByTagName('td')[columnIndex];

            let xValue = parseInt(x.innerText.trim()) || 0;
            let yValue = parseInt(y.innerText.trim()) || 0;

            if (sortOrder === 0) {
                // Sort in ascending order
                if (xValue > yValue) {
                    shouldSwitch = true;
                    break;
                }
            } else {
                // Sort in descending order
                if (xValue < yValue) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

function updateSortIndicator(header, sortOrder) {
    // Remove any existing arrow indicators
    $('th').find('.arrow-indicator').remove();

    // Add an arrow indicator to the clicked header
    const arrow = sortOrder === 0 ? '↓' : '↑'; // Invert the arrow order
    $(header).append(`<span class="arrow-indicator">${arrow}</span>`);
}

getUsers().then(data => {
    generateTable(data);
});

function handleFileSelect(event) {
    const file = event.target.files[0];

    if (file) {
        // Check if the file type is valid (in this example, only .json files are accepted)
        if (file.type !== 'application/json') {
            // Display an error message
            const errorNotice = document.getElementById('errorNotice');
            errorNotice.style.display = 'block';
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            const content = e.target.result;
            const json = JSON.parse(content);

            // Process the JSON data as needed, e.g., update the table with the new data
            generateTable(json);

            // Show the upload notice
            const uploadNotice = document.getElementById('uploadNotice');
            uploadNotice.style.display = 'block';

            // Hide the notice after a few seconds (e.g., 5 seconds)
            setTimeout(function () {
                uploadNotice.style.display = 'none';
            }, 5000);

            // Clear the file input to allow re-uploading the same file
            event.target.value = null;
        };

        reader.readAsText(file);
    }
}
