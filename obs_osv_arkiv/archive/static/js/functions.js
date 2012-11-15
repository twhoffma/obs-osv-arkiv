// JavaScript Document

$('nav').isotope({
  // options
  itemSelector : '.emne',
  layoutMode : 'fitRows'
});

$('nav').isotope({
  itemSelector: '.emne',
  masonry: {
    columnWidth: 120,
    cornerStampSelector: '.corner-stamp'
  }
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