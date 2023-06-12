$(document).foundation();

jq2 = jQuery.noConflict();
jq2(function ($) {
    var squareBox = $('.square-box').width();
    var recBox = $('.rec-box').width();
    var xRecBox = $('.x-rec-box').width();
    var listBox = $('.list-box').width();

    $('.square-box').height(squareBox);
    $('.rec-box').height(recBox / 1.6);
    $('.x-rec-box').height(xRecBox / 7);
    $('.list-box').height(listBox / 1.47);



    // handling the scroll button appearance.
    var  scroll = $(".to-top");
    $(window).scroll(function () {
       if ($(this).scrollTop() >= 200){
           scroll.fadeIn(500);
       } else {
           scroll.fadeOut(500);
       }
    });
    // animating the scroll button.
    scroll.click(function () {
          $("body,html").animate({
              scrollTop:0
          },950);
   });
});