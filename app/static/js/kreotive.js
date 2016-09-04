 $(document).ready(function() {

     $("#sign-in").popover({
         html: true,
         placement: "bottom",
         content: function () {
             return $("#log-in-form").html();
         }
     });

});


