/**
 * Mediaview page initialization.
 */

$(document).ready(function() {

    var $ts = $('#thumb-selector-inner');
    var $sup = $('#scroll-up');
    var $sdn = $('#scroll-down');

    $('#mediaview').mediaview();

    $('#toggle-details').click(function() {

        var details = $('.infoboks');
        $(this).toggleClass('active');

        if (details.is(':visible')) {
            details.hide('slide', { direction: 'right' }, 'fast');
        } else {
            details.show('slide', { direction: 'right' }, 'fast');
        }

    });

    $sup.click(function() {
        $ts[0].scrollTop -= 100;
    });

    $sdn.click(function() {
        $ts[0].scrollTop += 100;
    });

});
