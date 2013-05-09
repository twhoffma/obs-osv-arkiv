// JavaScript Document

$('#main-nav').isotope({
  // options
  itemSelector : '.cat',
  layoutMode : 'fitRows'
});


$('#item-info-wrapper').isotope({
  // options
  itemSelector : '.infoboks',
  layoutMode : 'masonry'
});


$('#content').isotope({
  // options
  itemSelector : '.thumb',
  layoutMode : 'masonry'
});

var $container = $('#content');

$container.imagesLoaded( function(){
  $container.isotope({
    // options...
  });
});


$(function(){
    $('a.toggle').click(function(){
      $('#infobox').animate({
       width: 'toggle'
      });
    });
});
