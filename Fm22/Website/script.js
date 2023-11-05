//wachten tot dat de DOM klaar is met inladen
$(document).ready(function () {
    let sortOrder = 0; // sort order 0 maken met oplopende sort

    // wanneer de goal header wordt geklikt 
    $('#container').on('click', 'th', function () {
        const columnIndex = this.cellIndex;

        if (columnIndex === 2) { // controleren of het de goal index is 
            sortTable(columnIndex, sortOrder);
            sortOrder = 1 - sortOrder; // kijkt welke sort order het is: Aflopend, Oplopend
            updateSortIndicator(this, sortOrder);
        }
    });
});

//haalt de json op vanuit de API URL
async function getplayers() {
    try {
        const response = await fetch(
            'http://127.0.0.1:8000/data', //API URL
            {
                method: 'GET',
            },
        );
        // controleerd of we een reactie krijgen van de URL
        if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
        }
        // wachten op json response om het in een const te zetten
        const data = await response.json();

        return data; // krijgen de data terug
    } catch (error) {
        console.log(error); // errors tijdens de fetch worden gelogd
    }
}
// html tabel generen op basis van de json 
function generateTable(data) {
    // maken van de tabel een string
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
    // door de json bestand heen loopen om alles eruit te halen
    Object.entries(data).map(player => {
        // goals omzetten naar een int
        const goals = parseInt(player[1].Dlp);

        // row maken voor elke speler
        table += `
        <tr>
          <td>${player[1].Naam}</td>
          <td>${player[1].Club}</td>
          <td>${isNaN(goals) ? 'N/A' : goals}</td> 
          <td>${player[1].xG}</td>
        </tr>
      `;
    });

    table += `
      </tbody>
    </table>
    `;
    //container element in de DOM
    const container = document.getElementById('container');
    //maakt de table string naar innerhtml
    container.innerHTML = table;
}
// functie om de tabel te sorteren op basis van column en op of af(lopend)
function sortTable(columnIndex, sortOrder) {
    let table, rows, switching, i, x, y, shouldSwitch;
    //pakt tabel element van DOM
    table = document.querySelector('#container table');
    //controleerd wisseling van de rows
    switching = true;

    while (switching) {
        switching = false;
        // alle rows van het tabel pakken
        rows = table.getElementsByTagName('tr');

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            //pakt de cel van de huidige row voor de gesorteerde column
            x = rows[i].getElementsByTagName('td')[columnIndex];
            y = rows[i + 1].getElementsByTagName('td')[columnIndex];
            // zet getallen om naar intergers
            let xValue = parseInt(x.innerText.trim()) || 0;
            let yValue = parseInt(y.innerText.trim()) || 0;

            if (sortOrder === 0) {
                // Sorteerd oplopend
                if (xValue > yValue) {
                    shouldSwitch = true;
                    break;
                }
            } else {
                // Sorteerd aflopend
                if (xValue < yValue) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            //veranderd posities van de rows om te sorteren
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            // aangeven dat er gesorteerd kan worden
            switching = true;
        }
    }
}
// functie om een sorteer pijl weertegeven
function updateSortIndicator(header, sortOrder) {
    // verwijderd huidige pijl
    $('th').find('.arrow-indicator').remove();

    // voegt pijl toe aan de geselecteerde column
    const arrow = sortOrder === 0 ? '↓' : '↑'; // veranderd de pijl volgorde
    $(header).append(`<span class="arrow-indicator">${arrow}</span>`);
}
// maakt de tabel met de json data
getplayers().then(data => {
    generateTable(data);
});
//upload bestand functie
async function uploadFile(file) {
    //maakt een form die we kunnen opsturen
    const formData = new FormData();
    formData.append('file', file);

    try {
        //post request naar de api
        const response = await fetch('http://127.0.0.1:8000/upload/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        //parsed de data als json
        const data = await response.json();
        console.log(data);

        // na het uploaden update de form met de nieuwe data
        const newData = await getplayers();
        generateTable(newData);
    } catch (error) {
        console.log(error);
    }
}

// Event listener voor wanneer het bestand veranderd
document.getElementById('uploadbtn').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        uploadFile(file);
    }
});
