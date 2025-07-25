const searchinput = document.querySelector('.search-input');
const resultsContainer = document.querySelector('.results-container');
let debounceTimer;

searchinput.addEventListener('input', (e) => {
    const text = e.target.value.trim();

    clearTimeout(debounceTimer);

    if (text !== '') {
        debounceTimer = setTimeout(() => {
            get_search(text);
        }, 2000);
    } else {
        resultsContainer.innerHTML = ''; // clear if input is empty
    }
});

async function get_search(search) {
    try {
        let response = await fetch('/search/' + search + '/');
        if (!response.ok) throw new Error("HTTP error " + response.status);

        let info = await response.json();
        info = info.drinks;
        render_results(info.slice(0, 5));  // show top 5 results
    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function render_results(results) {
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="result-item">No results found.</div>';
        return;
    }

    results.forEach(item => {
        const imgSrc = item.drinkimg || 'https://via.placeholder.com/50';
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';

        resultDiv.innerHTML = `
            <img class="result-img" src="${imgSrc}" alt="${item.drinkname}">
            <span class="result-title">${item.drinkname}</span>
        `;

        resultDiv.addEventListener('click', () => {
            alert(`You selected: ${item.drinkname}`);
        });

        resultsContainer.appendChild(resultDiv);
    });
}

