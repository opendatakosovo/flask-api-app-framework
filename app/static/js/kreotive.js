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


