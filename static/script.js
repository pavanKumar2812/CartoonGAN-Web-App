$(document).ready(function () {
    console.log("Hi");
    $(".VideoContainer").hide();
    $(".image_container").show();
    $("#Menus").accordion({
      heightStyle: "content",
      activate: function (event, ui) {
        var Caption = ui.newHeader.text();
        $(".VideoContainer").hide();
        $(".image_container").hide();
  
        if (Caption == "Raw Video") {
          $(".VideoContainer").show();
          $(".image_container").hide();
          $(".Video").attr("src", "/RawVideo");
        }
        else if (Caption == "Cartoon Video") {
          $(".VideoContainer").show();
          $(".image_container").hide();
          $(".Video").attr("src", "/CartoonVideo");
        }
        else if (Caption == "Image") {
            $(".VideoContainer").hide();
            $(".image_container").show();
            $(".Video").attr("src", "/CartoonVideo");
        }
      }
    });

    $('#upload-form').on('submit', function (e) {
      e.preventDefault();
  
      const formData = new FormData(this);
  
      $.ajax({
          url: '/cartoonize',
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function (response) {
              if (response.image_url) {
                  $('#cartoon-image').attr('src', response.image_url).show();
              } else {
                  alert('Failed to retrieve cartoonized image.');
              }
          },
          error: function (err) {
              console.error('Error:', err.responseText);
              alert('An error occurred: ' + err.responseText);
          }
      });
  });  

});
