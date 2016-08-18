 $(document).ready(function(){

    $("#sign-in").popover({
        html : true, 
        placement: "bottom",
        content: function() {
          return $("#log-in-form").html();
        }
    });
});
 

  $(document).ready(function(){
       $(".menu-icons a").click(function (e) {
          e.preventDefault();
      });

  });



$(document).ready(function() {
    $(".close-icon").click(function () {
        $("#un-registered").fadeOut(1000)
    });
});


