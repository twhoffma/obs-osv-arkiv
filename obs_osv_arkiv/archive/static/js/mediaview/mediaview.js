/**
 * Mediaview page initialization.
 */

$(document).ready(function() {

    var $doc = $(document);
    var $ts = $('#thumb-selector-inner');
    var $sup = $('#scroll-up');
    var $sdn = $('#scroll-down');
    var $mediaview = $('#mediaview');
    var $sidebar = $('#sidebar');

    $mediaview.mediaview();

    $('#toggle-details').click(function() {

        var details = $('#infobox');
        $(this).toggleClass('active');

        if (details.is(':visible')) {
            details.hide('slide', { direction: 'right' }, 400);
        } else {
            details.show('slide', { direction: 'right' }, 400);
        }

    });

    $('#toggle-fullscreen').click(function() {
        $doc.fullScreen(true);
    });

    $('#controls #zoom-in').click(function() {
        $mediaview.mediaview('zoom', 1.2);
    });

    $('#controls #zoom-out').click(function() {
        $mediaview.mediaview('zoom', -1.2);
    });

    $('#controls #rotate').click(function() {
        $mediaview.mediaview('rotate', 0);
    });

    $('#controls #reset').click(function() {
        $mediaview.mediaview('reset');
    });

    $doc.bind('fullscreenchange', function() {
        $sidebar.toggle(!($doc.fullScreen()));
    });

    $sup.click(function() {
        $ts[0].scrollTop -= 100;
    });

    $sdn.click(function() {
        $ts[0].scrollTop += 100;
    });

});
