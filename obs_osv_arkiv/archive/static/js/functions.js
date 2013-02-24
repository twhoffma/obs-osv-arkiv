// JavaScript Document

$('nav').isotope({
  // options
  itemSelector : '.cat',
  layoutMode : 'fitRows'
});

$('nav #nav').isotope({
  itemSelector: '.cat cat-lvl-3',
  masonry: {
    columnWidth: 120,
    cornerStampSelector: '.corner-stamp .corner-stamp2'
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

//Flexslider
/*$(window).load(function() {
  $('.flexslider').flexslider({
    animation: "slide",
	animationSpeed: 0,    
	controlNav: "thumbnails",
	slideshow: false,
	touch: true,
	video: true,
  });
});
*/
