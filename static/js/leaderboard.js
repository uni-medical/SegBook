// static/js/leaderboard.js

let currentData = [];

function loadLeaderboard(filename) {
    // Remove 'active' class from all buttons
    document.querySelectorAll('.leaderboard-menu button').forEach(btn => btn.classList.remove('active'));
    // Add 'active' class to the clicked button
    event.target.classList.add('active');

    fetch(`static/data/${filename}`)
        .then(response => response.json())
        .then(data => {
            currentData = data;
            populateTable();
        })
        .catch(error => console.error('Error loading leaderboard data:', error));
}

function populateTable() {
    const table = document.getElementById('leaderboardTable');
    const tbody = table.querySelector('tbody');
    const thead = table.querySelector('thead');
    tbody.innerHTML = '';
    thead.innerHTML = '';

    if (currentData.length === 0) return;

    // Assume first object keys are headers
    const headers = currentData[0];
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Data rows
    for (let i = 1; i < currentData.length; i++) {
        const row = currentData[i];
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    }
}

// Load the main leaderboard on page load
window.onload = function() {
    loadLeaderboard('main.json');
};
