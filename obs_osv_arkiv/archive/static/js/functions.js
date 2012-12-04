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

$(function(){
        $(".thumb").hover(function(){
                            $(this).fadeTo('fast',0.3);   
                            },
                            function(){
                            $(this).fadeTo('fast',1);       
                            });
});

var $container = $('#content');

$container.imagesLoaded( function(){
  $container.isotope({
    // options...
  });
});