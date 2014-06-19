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
    var $controls = $('#controls');
    var rotate_id = null;
    var zoom_id = null;
    var controls_id = null;
    var controls_visible_locked = false;
    var controls_visible = true;

    $mediaview.mediaview();

    /**
     * Automatically show/hide fullscreen controls on mousemove.
     */
    $doc.mousemove(function() {

        if (!$doc.fullScreen()) {
            return;
        }

        if (!controls_visible) {
            controls_visible = true;
            $controls.stop(true, true).show();
        }

        if (controls_id !== null) {
            clearTimeout(controls_id);
            if (controls_visible_locked) {
                controls_id = null;
            }
        }

        if (controls_visible && !controls_visible_locked) {
            controls_id = setTimeout(function() {
                controls_visible = false;
                $controls.fadeOut();
            }, 500);
        }

    });

    /**
     * Lock controls on-screen when mouse is hovering.
     */
    $controls.mouseenter(function() {
        controls_visible_locked = true;
    });

    /**
     * Unlock controls on-screen when mouse is leaving.
     */
    $controls.mouseleave(function() {
        controls_visible_locked = false;
    });

    $toggle_details.click(function() {

        $(this).toggleClass('active');

        if ($details.is(':visible')) {
            $details.hide('slide', { direction: 'right' }, 400);
        } else {
            $details.show('slide', { direction: 'right' }, 400);
        }

    });

    var fullscreen_detect = function() {
        if (!($doc.fullScreen())) {
            alert("Nettleseren du bruker, støtter ikke fullskjerm. Vennligst oppdater, eller om mulig, bytt nettleser for å bruke denne funksjonen. Støttede nettlesere er bl.a. Google Chrome og Mozilla Firefox.");
        }
    };

    $('#toggle-fullscreen').click(function() {
        $doc.fullScreen(true);
        setTimeout(fullscreen_detect, 1000);
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
            zoom_id = setInterval(function() { do_zoom(1.005); }, 5);
        }
    });

    $('#controls #zoom-out').mousedown(function() {
        if (zoom_id === null) {
            zoom_id = setInterval(function() { do_zoom(-1.005); }, 5);
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
            $doc.trigger('mousemove');
        } else {
            controls_visible = true;
            $controls.stop(true, true).show();
        }
    });

    $sup.click(function() {
        $ts[0].scrollTop -= 100;
    });

    $sdn.click(function() {
        $ts[0].scrollTop += 100;
    });

});
