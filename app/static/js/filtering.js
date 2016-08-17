

  $(document).ready(function() {

      var $img;
      $img = $('.icon').click(function () {
          if (this.id == 'articles') {
              $('#articles > div >div').fadeIn(450);
          } else {
              var $el = $('.' + this.id).fadeIn(450);
              $('#articles > div >div').not($el).hide();
          }
          $img.removeClass('active');
          $(this).addClass('active');
      });

  });