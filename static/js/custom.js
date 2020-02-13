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
});
