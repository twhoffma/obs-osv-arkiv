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
