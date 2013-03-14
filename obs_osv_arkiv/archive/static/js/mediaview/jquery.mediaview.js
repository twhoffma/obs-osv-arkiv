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
     * Active canvas' settings: pan, zoom, modes etc.
     */
    var settings = {};

    /**
     * How fast does the wheel zoom?
     */
    var SCROLL_FACTOR = 1.04;

    /**
     * Maximal zoom factor
     */
    var MAX_ZOOM = 1.25;

    /**
     * Viewport width and height
     */
    var view_width = 0;
    var view_height = 0;

    /**
     * Pre-loading icon
     */
    var loading = $('<img/>').attr('src', '/static/images/ajax-loader.gif').addClass('loading');


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

                /* Initialize settings array for all canvases */
                piclist.children('li').children('canvas').each(function() {
                    $(this).data('settings', {});
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

                settings = canvas.data('settings');

                /* Callback for image load */
                var load_port = function(image) {
                    canvas[0].width = view_width;
                    canvas[0].height = view_height;
                    image.hide().insertAfter(canvas);
                    ctx = canvas[0].getContext('2d');

                    if (!settings.length) {

                        settings.last_mouse = [0, 0];
                        settings.pan = [0, 0];
                        settings.zoom = 1.0;
                        settings.rotate = 0;
                        settings.mousedown = false;
                        settings.mousemode = null;

                        var draw = function() {
                            ctx.setTransform(1, 0, 0, 1, 0, 0);
                            ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);

                            ctx.translate(view_width / 2, view_height / 2);
                            ctx.rotate(settings.rotate * (Math.PI / 180));
                            ctx.translate(-view_width / 2, -view_height / 2);

                            ctx.scale(settings.zoom, settings.zoom);
                            ctx.drawImage(image[0], settings.pan[0] / settings.zoom, settings.pan[1] / settings.zoom);
                        };

                        var mouse_event = function(ev, mode, deltaX, deltaY) {

                            if (mode == 'pan') {

                                var cos = Math.cos(settings.rotate * (Math.PI / 180));
                                var sin = Math.sin(settings.rotate * (Math.PI / 180));

                                settings.pan[0] += (deltaX * cos) + (deltaY * sin);
                                settings.pan[1] += (deltaY * cos) - (deltaX * sin);

                            } else if (mode == 'rotate') {

                                settings.rotate = (settings.rotate + (0.5 * (deltaX + deltaY))) % 360;

                            } else if (mode == 'zoom') {

                                var scroll_delta = 1;
                                if (deltaY < 0) {
                                    /* zoom out */
                                    scroll_delta = 1 / SCROLL_FACTOR;
                                } else if (deltaY > 0 && settings.zoom < MAX_ZOOM) {
                                    /* zoom in */
                                    scroll_delta = SCROLL_FACTOR;
                                }

                                settings.zoom = settings.zoom * scroll_delta;

                                /* Zoom to cursor */
                                var im_x = ev.pageX - settings.pan[0];
                                var im_y = ev.pageY - settings.pan[1];
                                var new_x = im_x * scroll_delta;
                                var new_y = im_y * scroll_delta;

                                settings.pan[0] -= (new_x - im_x);
                                settings.pan[1] -= (new_y - im_y);

                            }

                            draw();

                        };

                        /* Bind zoom event */
                        canvas.mousewheel(function(ev, delta, deltaX, deltaY) {
                            mouse_event(ev, 'zoom', deltaX, deltaY);
                        });

                        /* Panning requires several events */
                        var stopmouse = function() {
                            settings.mousedown = false;
                        };
                        canvas.mousedown(function(ev) {
                            settings.mousedown = true;
                            settings.last_mouse = [ev.pageX, ev.pageY];
                            if (ev.metaKey && !ev.ctrlKey) {
                                settings.mousemode = 'zoom';
                            } else if (ev.ctrlKey && !ev.metaKey) {
                                settings.mousemode = 'rotate';
                            } else {
                                settings.mousemode = 'pan';
                            }
                            ev.stopPropagation();
                            ev.preventDefault();
                        });
                        canvas.mouseup(stopmouse);
                        canvas.mouseleave(stopmouse);
                        canvas.mousemove(function(ev) {
                            if (!settings.mousedown) {
                                return;
                            }
                            var delta = [ ev.pageX - settings.last_mouse[0], ev.pageY - settings.last_mouse[1] ];
                            mouse_event(ev, settings.mousemode, delta[0], delta[1]);
                            settings.last_mouse = [ev.pageX, ev.pageY];
                        });

                        /* Initial zoom level based on image and viewport dimensions */
                        var x = view_width / image[0].width;
                        var y = view_height / image[0].height;
                        //if (x < 1 || y < 1) {
                            if (x < y) {
                                settings.zoom = x;
                            } else {
                                settings.zoom = y;
                            }
                        //}

                        /* Center image */
                        var x = (view_width / 2) - ((image[0].width * settings.zoom) / 2);
                        var y = (view_height / 2) - ((image[0].height * settings.zoom) / 2);
                        settings.pan = [x, y];

                    }

                    draw();
                };

                var image = canvas.siblings('img');

                if (image.length == 0) {
                    /* Pre-load thumbnail into viewport for quick view */
                    image = img.clone();
                    image.load(function() {
                        load_port(image);
                        var loader = loading.clone().insertBefore(canvas);

                        /* Load the real image */
                        image = $('<img/>').attr('src', canvas.attr('data-image'));
                        image.load(function() { loader.remove(); load_port(image); });
                    });
                } else {
                    load_port(image);
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
