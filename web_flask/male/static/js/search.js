function handleSearch(event) {
    event.preventDefault(); // Prevent the default form submission

    const input = document.getElementById('searchInput').value.toLowerCase().trim();

    let redirectUrl;

    if (input === 'male') {
        redirectUrl = "dashboard";
    } else if (input === 'hostels') {
        redirectUrl = "male";
    } else if (input === 'contact') {
        redirectUrl = "{{ url_for('contact') }}";
    } else {
        redirectUrl = "dashboard";
    }

    window.location.href = redirectUrl;
}
