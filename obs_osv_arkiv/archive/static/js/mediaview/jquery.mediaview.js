/**
 * MediaView plugin
 *
 * @author: Kim Tore Jensen <kim@incendio.no>
 */

(function($) {

    /**
     * The active canvas context for panning, zooming etc.
     */
    var ctx = null;

    /**
     * Viewport width and height
     */
    var view_width = 0;
    var view_height = 0;

    var methods = {

        init : function(options) {

            return this.each(function() {

                var $this = $(this);
                var sidebar = $this.children('nav');
                var piclist = $this.children('#container').children('ul');

                /* Build thumbnail selector */
                var thumbs = sidebar.children('.thumb-selector');
                var originals = piclist.children('li');

                originals.each(function() {
                    var th = $('<img/>').attr('src', $(this).attr('data-thumb'));
                    var soulmate = $(this);

                    thumbs.append(th);

                    /* Exchange blood */
                    th.data('soulmate', soulmate);
                    soulmate.data('soulmate', th);

                    /* Bind click event */
                    th.click(function() {
                        $this.mediaview('activate', th);
                    });

                });

                /* Maintain viewport dimensions */
                $this.mediaview('detect_dimensions');
                $(window).resize(function() {
                    $this.mediaview('detect_dimensions');
                });

                /* Show the first image in the series */
                $this.mediaview('activate', thumbs.children().slice(0, 1));

            });

        },

        activate : function(img) {

            return this.each(function() {

                var $this = $(this);
                var soulmate = img.data('soulmate');

                img.addClass('active').siblings().removeClass('active');
                soulmate.show().siblings().hide();

                /* Initialize canvas, if applicable */
                var canvas = soulmate.children('canvas').slice(0, 1);
                if (canvas.length == 0) {
                    return;
                }

                var image = canvas.siblings('img');

                /* Callback for image load */
                var callback = function() {
                    canvas[0].width = image[0].width;
                    canvas[0].height = image[0].height;
                    image.hide().insertAfter(canvas);
                    ctx = canvas[0].getContext('2d');

                    if (!canvas.data('initialized')) {

                        /* Bind zoom event */
                        canvas.mousewheel(function(e, delta, deltaX, deltaY) {
                            var zoom = canvas.data('zoom');
                            var pan = canvas.data('pan');
                            if (deltaY < 0) {
                                zoom = zoom / 1.15;
                                pan[0] *= 1.15;
                                pan[1] *= 1.15;
                            } else if (deltaY > 0 && zoom < 1) {
                                zoom = zoom * 1.15;
                                pan[0] /= 1.15;
                                pan[1] /= 1.15;
                            }
                            ctx.setTransform(1, 0, 0, 1, 0, 0);
                            ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);

                            ctx.scale(zoom, zoom);
                            ctx.drawImage(image[0], pan[0], pan[1]);

                            canvas.data('pan', pan);
                            canvas.data('zoom', zoom);
                        });

                        /* Initial zoom level based on image and viewport dimensions */
                        var zoom = 1.0;
                        var padding = 50;
                        var x = view_width / (image[0].width + padding);
                        var y = view_height / (image[0].height + padding);
                        if (x < 1 || y < 1) {
                            if (x < y) {
                                zoom = x;
                            } else {
                                zoom = y;
                            }
                        }
                        canvas.data('zoom', zoom);

                        /* Center image */
                        var x = (view_width / 2) - (zoom * (image[0].width / 2));
                        var y = (view_height / 2) - (zoom * (image[0].height / 2));
                        var pan = [x / zoom, y / zoom];
                        canvas.data('pan', pan);

                        canvas.data('rotate', 0);
                        canvas.data('initialized', true);

                    }

                    /* Clear canvas */
                    ctx.setTransform(1, 0, 0, 1, 0, 0);
                    ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);

                    var zoom = canvas.data('zoom');
                    var pan = canvas.data('pan');
                    ctx.scale(zoom, zoom);
                    ctx.drawImage(image[0], pan[0], pan[1]);
                };

                if (image.length == 0) {
                    /* Bootstrap */
                    var image = $('<img/>').attr('src', canvas.attr('data-image'));
                    canvas.data('initialized', false);
                    image.load(callback);
                } else {
                    callback();
                }

            });

        },

        detect_dimensions : function(options) {

            return this.each(function() {

                var ul = $(this).children('#container').children('ul');

                view_width = ul.width();
                view_height = ul.height();

            });

        }

    };

    $.fn.mediaview = function(method) {
        
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.mediaview');
        }        
    
    };

})(jQuery);
