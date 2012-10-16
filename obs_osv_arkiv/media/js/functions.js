//isotope code

$('nav').isotope({
  // options
    itemSelector : '.emne2',
    layoutMode : 'fitRows'
});

$(document).ready(function () {
	"use strict";
    var $container = $('nav');
    $container.isotope({
		layoutMode: 'fitRows',
        animationOptions: {
            duration: 100,
            easing: 'linear',
            queue: false
        }
    });
});

$(function () {
	"use strict";

	// Accordion
	$("#accordion").accordion({ header: "h3" });
});

//fileinput
$('input[type="text"]').keypress(function(e){
    e.preventDefault();    
});
    
$('.theFileInput').change(function(){
    $('.browseText').val($(this).val());
});

// if condition for Webkit and IE
if($.browser.webkit || $.browser.msie){
    $('.theFileInput').css('left', '190px');
}​