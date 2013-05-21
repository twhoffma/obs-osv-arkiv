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
    var $toggle_details = $('#toggle-details');
    var $details = $('#infobox');
    var rotate_id = null;
    var zoom_id = null;

    $mediaview.mediaview();

    $toggle_details.click(function() {

        $(this).toggleClass('active');

        if ($details.is(':visible')) {
            $details.hide('slide', { direction: 'right' }, 400);
        } else {
            $details.show('slide', { direction: 'right' }, 400);
        }

    });

    $('#toggle-fullscreen').click(function() {
        $doc.fullScreen(true);
    });

    var do_zoom = function(factor) {
        $mediaview.mediaview('zoom', factor);
    };

    var clear_zoom = function() {
        if (zoom_id !== null) {
            clearInterval(zoom_id);
            zoom_id = null;
        }
    };

    $('#controls #zoom-in').mousedown(function() {
        if (zoom_id === null) {
            zoom_id = setInterval(do_zoom, 5, 1.005);
        }
    });

    $('#controls #zoom-out').mousedown(function() {
        if (zoom_id === null) {
            zoom_id = setInterval(do_zoom, 5, -1.005);
        }
    });

    $('#controls #zoom-in').mouseout(clear_zoom);
    $('#controls #zoom-in').mouseup(clear_zoom);
    $('#controls #zoom-out').mouseout(clear_zoom);
    $('#controls #zoom-out').mouseup(clear_zoom);

    var do_rotate = function() {
        $mediaview.mediaview('rotate', 0.75);
    };

    var clear_rotate = function() {
        if (rotate_id !== null) {
            clearInterval(rotate_id);
            rotate_id = null;
        }
    };

    $('#controls #rotate').mousedown(function() {
        if (rotate_id === null) {
            rotate_id = setInterval(do_rotate, 5);
        }
    });

    $('#controls #rotate').mouseout(clear_rotate);
    $('#controls #rotate').mouseup(clear_rotate);

    $('#controls #reset').click(function() {
        $mediaview.mediaview('reset');
    });

    $doc.bind('fullscreenchange', function() {
        $sidebar.toggle(!($doc.fullScreen()));
        if ($doc.fullScreen()) {
            $toggle_details.removeClass('active');
            $details.hide();
        }
    });

    $sup.click(function() {
        $ts[0].scrollTop -= 100;
    });

    $sdn.click(function() {
        $ts[0].scrollTop += 100;
    });

});
