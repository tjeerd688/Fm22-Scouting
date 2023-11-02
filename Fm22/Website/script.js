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

//regelt het uploaden van de CSV op de website
function handleFileSelect(event) {
    const file = event.target.files[0];

    if (file) {
        // controleerd of het bestandstype een csv is
        if (file.type !== 'text/csv') {
            // error als het geen csv is
            const errorNotice = document.getElementById('errorNotice');
            errorNotice.style.display = 'block';
            setTimeout(function () {
                errorNotice.style.display = 'none';
            }, 3000);
            return;
        }
        // maakt filereader
        const reader = new FileReader();

        // geeft aan dat het bestand is geupload
        const uploadNotice = document.getElementById('uploadNotice');
        uploadNotice.style.display = 'block';

        //haalt de melding weg na 3 seconden
        setTimeout(function () {
            uploadNotice.style.display = 'none';
        }, 3000);

        // event listener als het bestand geladen is
        reader.onload = function (e) {
            //leest het bestand
            const content = e.target.result;
            //parst de csv
            Papa.parse(content, {
                header: true, // eerste row met headers
                dynamicTyping: true, // veranderd de datatypes naar de verwachte types

            });



            // melding gaat weg na 3 sec


            // input bestand word weggehaald zodat er een volgende ingevoerd kan worden
            event.target.value = null;
        };
    }
}
