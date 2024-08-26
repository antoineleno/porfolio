document.addEventListener('DOMContentLoaded', () => {
    // Function to fetch country data and populate the select element
    function fetchCountries() {
        fetch('https://restcountries.com/v3.1/all')
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById('country');
                if (selectElement) {
                    data.sort((a, b) => a.name.common.localeCompare(b.name.common)); // Sort alphabetically
                    data.forEach(country => {
                        const option = document.createElement('option');
                        option.value = country.cca2; // Country code (e.g., 'US')
                        option.textContent = country.name.common; // Country name (e.g., 'United States')
                        selectElement.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error fetching country data:', error));
    }

    // Function to handle menu toggle
    function setupMenuToggle() {
        const menuToggle = document.querySelector('.menu-toggle');
        const containerMenu = document.querySelector('.container-menu');

        if (menuToggle && containerMenu) {
            menuToggle.addEventListener('click', () => {
                containerMenu.classList.toggle('active');
            });
        }
    }

    // Initialize functions
    fetchCountries();
    setupMenuToggle();
});

