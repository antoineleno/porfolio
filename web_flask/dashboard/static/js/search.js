function handleSearch(event) {
    event.preventDefault(); // Prevent the default form submission

    const input = document.getElementById('searchInput').value.toLowerCase().trim();

    let redirectUrl;

    if (input === 'home') {
        redirectUrl = "dashboard";
    } else if (input === 'hostels' || input === 'male')  {
        redirectUrl = "/campusstay/admin/dashboard/male";
    } else if (input === 'female') {
        redirectUrl = "/campusstay/admin/dashboard/female";
    } else if (input === 'leaves') {
        redirectUrl = "/campusstay/admin/dashboard/leaves";
    } else if (input === 'inquiries') {
        redirectUrl = "/campusstay/admin/dashboard/inquiries";
    } else if (input === 'report') {
        redirectUrl = "/campusstay/admin/dashboard/report";
    } else if (input === 'search') {
        redirectUrl = "/campusstay/admin/dashboard/search";
    } else {
        redirectUrl = "dashboard";
    }

    window.location.href = redirectUrl;
}
