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
