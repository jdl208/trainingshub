$(document).ready(function() {
    $("#navbtn").click(function() {
        $(".overlay").addClass("active");
        $("#mySidenav").width(250);
    });

    $(".overlay").click(function() {
        $(".overlay").removeClass("active");
        $("#mySidenav").width(0);
    });

    $(".closebtn").click(function() {
        $(".overlay").removeClass("active");
        $("#mySidenav").width(0);
    });
    // Make tablerows clickable as a link
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
    // change active tab on account page of user and
    $("#course-nav a").on("click", function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
    $("#upcoming").on("click", function() {
        $("#upcoming-courses").removeClass("d-none");
        $("#past-courses").addClass("d-none");
        $("#past").addClass("text-white");
        $("#upcoming").removeClass("text-white");
    });
    $("#past").on("click", function() {
        $("#past-courses").removeClass("d-none");
        $("#upcoming-courses").addClass("d-none");
        $("#upcoming").addClass("text-white");
        $("#past").removeClass("text-white");
    });
});
