$(window).load(function() {

    var $container = $('#content');

    $('#main-nav').isotope({
        itemSelector : '.cat',
        layoutMode : 'fitRows'
    });

    $container.isotope({
        itemSelector : '.thumb',
        layoutMode : 'masonry'
    });

    $container.imagesLoaded(function() {
        $container.isotope({});
    });

});

$(function(){
    $('a.toggle').click(function(){
      $('#infobox').fadeToggle("fast");
    });
});

$( ".mobileinfo" ).click(function() {
  $( "#infobox" ).slideToggle( "normal", function() {
    // Animation complete.
  });
});
