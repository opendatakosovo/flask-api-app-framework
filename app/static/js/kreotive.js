 $(document).ready(function() {

     $("#sign-in").popover({
         html: true,
         placement: "bottom",
         content: function () {
             return $("#log-in-form").html();
         }
     });

     $(".menu-icons a").click(function (e) {
         e.preventDefault();
     });


     var div = $('#un-registered');

     $('.fa-close').on('click', function () {
         div.fadeOut();
     });

});


