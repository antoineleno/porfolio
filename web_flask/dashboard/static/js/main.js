(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });


    // Progress Bar
    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Calendar
    $('#calender').datetimepicker({
        inline: true,
        format: 'L'
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav : false
    });


    // Fetch data and initialize charts
    $.getJSON('/campusstay/api/chart-data')
        .done(function(data) {
            // Update Bar Chart for Male
            var ctx4 = $("#bar-chart").get(0).getContext("2d");
            new Chart(ctx4, {
                type: "bar",
                data: {
                    labels: data.male.labels,  // Use labels from male data
                    datasets: [{
                        backgroundColor: [
                            "rgba(255, 159, 64, 0.7)",
                            "rgba(255, 206, 86, 0.7)",
                            "rgba(255, 99, 132, 0.7)",
                            "rgba(54, 162, 235, 0.7)",
                            "rgba(75, 192, 192, 0.7)",
                            "rgba(153, 102, 255, 0.7)",
                            "rgba(255, 159, 64, 0.7)",
                            "rgba(199, 199, 199, 0.7)",
                            "rgba(255, 206, 86, 0.7)",
                            "rgba(75, 192, 192, 0.7)",
                            "rgba(83, 102, 255, 0.7)",
                            "rgba(255, 99, 71, 0.7)",
                            "rgba(102, 255, 178, 0.7)"
                        ],
                        data: data.male.values,  // Use values from male data
                        label: 'Male Students'
                    }]
                },
                options: {
                    responsive: true
                }
            });

            // Update Bar Chart for Female
            var ctx5 = $("#bar-charts").get(0).getContext("2d");
            new Chart(ctx5, {
                type: "bar",
                data: {
                    labels: data.female.labels,  // Use labels from female data
                    datasets: [{
                        backgroundColor: [
                            "rgba(0, 156, 255, .7)",
                            "rgba(255, 99, 132, 0.7)",
                            "rgba(54, 162, 235, 0.7)",
                            "rgba(255, 206, 86, 0.7)",
                            "rgba(75, 192, 192, 0.7)",
                            "rgba(153, 102, 255, 0.7)",
                            "rgba(255, 159, 64, 0.7)",
                            "rgba(199, 199, 199, 0.7)",
                            "rgba(83, 102, 255, 0.7)",
                            "rgba(255, 99, 71, 0.7)",
                            "rgba(102, 255, 178, 0.7)"
                        ],
                        data: data.female.values,  // Use values from female data
                        label: 'Female Students'
                    }]
                },
                options: {
                    responsive: true
                }
            });

        }).fail(function() {
            console.error('Failed to fetch data.');
        });

})(jQuery);

