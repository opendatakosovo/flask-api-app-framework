 $(document).ready(function(){
    $('#LogInForm').popover()

    $("#signIn").popover({
        html : true, 
        placement: "bottom",
        content: function() {
          return $("#LogInForm").html();
        }
    });
});