/**
 * Mediaview page initialization.
 */

$(document).ready(function() {

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

});
