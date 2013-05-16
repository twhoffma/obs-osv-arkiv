/**
 * MediaView plugin
 *
 * @author: Kim Tore Jensen <kim@incendio.no>
 */

(function($) {

    /**
     * The active canvas context for panning, zooming etc.
     */
    var canvas = null;
    var ctx = null;
    var canvas_image = null;
    var mininav = null;
    var mininav_ctx = null;

    /**
     * Active canvas' settings: pan, zoom, modes etc.
     */
    var settings = {};

    /**
     * Enable mininav?
     */
    var mininav_enabled = false;
    var base_ratio = 1;

    /**
     * How fast does the wheel zoom?
     */
    var SCROLL_FACTOR = 1.04;

    /**
     * Zoom limits
     */
    var MAX_ZOOM = 1.5;
    var MIN_ZOOM = 0.25;

    /**
     * Viewport width and height
     */
    var view_width = 0;
    var view_height = 0;

    /**
     * Pre-loading icon
     */
    var loading = $('<img/>').attr('src', '/static/images/ajax-loader.gif').addClass('loading');

    var draw = function() {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);

        ctx.translate(view_width / 2, view_height / 2);
        ctx.rotate(settings.rotate * (Math.PI / 180));
        ctx.translate(-view_width / 2, -view_height / 2);

        ctx.scale(settings.zoom, settings.zoom);
        ctx.drawImage(canvas_image[0], settings.pan[0] / settings.zoom, settings.pan[1] / settings.zoom);

        if (mininav_enabled) {
            mininav_draw();
        }
    };

    var mininav_draw = function() {
        mininav_ctx.setTransform(1, 0, 0, 1, 0, 0);
        mininav_ctx.clearRect(0, 0, mininav_canvas[0].width, mininav_canvas[0].height);

        mininav_ctx.translate(mininav[0].width / 2, mininav[0].height / 2);
        mininav_ctx.rotate(settings.rotate * (Math.PI / 180));
        mininav_ctx.translate(-mininav[0].width / 2, -mininav[0].height / 2);

        mininav_ctx.drawImage(mininav[0], 0, 0);

        /* Figure out viewport window. */
        var x1 = settings.pan[0];
        var y1 = settings.pan[1];
        var x2 = x1 + (canvas_image[0].width * settings.zoom);
        var y2 = y1 + (canvas_image[0].height * settings.zoom);

        var mini_x1 = 0;
        var mini_y1 = 0;
        var mini_x2 = mininav[0].width;
        var mini_y2 = mininav[0].height;

        if (x1 < 0) {
            mini_x1 = (-x1 / settings.zoom) / base_ratio;
        }
        if (y1 < 0) {
            mini_y1 = (-y1 / settings.zoom) / base_ratio;
        }
        if (x2 > view_width) {
            mini_x2 -= ((x2 - view_width) / base_ratio) / settings.zoom;
        }
        if (y2 > view_height) {
            mini_y2 -= ((y2 - view_height) / base_ratio) / settings.zoom;
        }

        mininav_ctx.fillRect(mini_x1, mini_y1, mini_x2-mini_x1, mini_y2-mini_y1);
        mininav_ctx.strokeRect(mini_x1, mini_y1, mini_x2-mini_x1, mini_y2-mini_y1);

    };
    var methods = {

        init : function(options) {

            return this.each(function() {

                var $this = $(this);
                var sidebar = $this.children('nav');
                var piclist = $this.children('#container').children('ul');

                /* Build thumbnail selector */
                var thumbs_loaded = 0;
                var thumbs = $('#thumb-selector');
                var originals = piclist.children('li');

                /* Re-detect dimensions when all thumbnails are loaded. */
                var thumb_load = function() {
                    if (++thumbs_loaded == originals.length) {
                        $this.mediaview('detect_dimensions');
                    }
                };

                originals.each(function() {
                    var th = $('<img/>').attr('src', $(this).attr('data-thumb'));
                    var soulmate = $(this);

                    thumbs.append(th);
                    th.one('load', thumb_load);

                    /* Exchange blood */
                    th.data('soulmate', soulmate);
                    soulmate.data('soulmate', th);

                    /* Bind click event */
                    th.click(function() {
                        $this.mediaview('activate', th);
                    });

                    /* Run load() event even if we missed it */
                    if (th[0].complete) {
                        th.load();
                    }

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
                canvas = soulmate.children('canvas').slice(0, 1);
                if (canvas.length == 0) {
                    return;
                }

                /* Set up thumbnail mini-navigation */
                if (mininav_enabled) {
                    var mininav = $('#thumb-navigator');
                    var thumb = img.clone().hide();
                    var mininav_canvas = $('<canvas/>');
                    var base_ratio = 1.0;
                    mininav.empty().append(thumb);
                    mininav.append(mininav_canvas);
                    mininav.appendTo(sidebar);
                }

                settings = canvas.data('settings');

                /* Callback for image load */
                var load_port = function(image) {
                    canvas_image = image;
                    canvas[0].width = view_width;
                    canvas[0].height = view_height;
                    image.hide().insertAfter(canvas);
                    ctx = canvas[0].getContext('2d');

                    if (mininav_enabled) {
                        mininav = img;
                        mininav_canvas[0].width = img[0].width;
                        mininav_canvas[0].height = img[0].height;
                        base_ratio = image[0].width / img[0].width;
                        mininav_ctx = mininav_canvas[0].getContext('2d');
                        mininav_ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                        mininav_ctx.strokeStyle = 'rgba(255, 0, 0, 1)';
                    }

                    if (!settings.length) {

                        settings.last_mouse = [0, 0];
                        settings.pan = [0, 0];
                        settings.zoom = 1.0;
                        settings.rotate = 0;
                        settings.mousedown = false;
                        settings.mininav_mousedown = false;
                        settings.mousemode = null;

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
                                if (deltaY < 0 && settings.zoom > MIN_ZOOM) {
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

                        /* Mininav panning is simpler */
                        if (mininav_enabled) {
                            var mininav_stopmouse = function() {
                                settings.mininav_mousedown = false;
                            };
                            mininav_canvas.mousedown(function(ev) {
                                settings.mininav_mousedown = true;
                                settings.mininav_last_mouse = [ev.pageX, ev.pageY];
                                ev.stopPropagation();
                                ev.preventDefault();
                            });
                            mininav_canvas.mouseup(mininav_stopmouse);
                            mininav_canvas.mouseleave(mininav_stopmouse);
                            mininav_canvas.mousemove(function(ev) {
                                if (!settings.mininav_mousedown) {
                                    return;
                                }
                                var delta = [ ev.pageX - settings.mininav_last_mouse[0], ev.pageY - settings.mininav_last_mouse[1] ];
                                delta[0] *= base_ratio * settings.zoom;
                                delta[1] *= base_ratio * settings.zoom;
                                var cos = Math.cos(settings.rotate * (Math.PI / 180));
                                var sin = Math.sin(settings.rotate * (Math.PI / 180));
                                settings.pan[0] -= (delta[0] * cos) + (delta[1] * sin);
                                settings.pan[1] -= (delta[1] * cos) - (delta[0] * sin);
                                draw();
                                settings.mininav_last_mouse = [ev.pageX, ev.pageY];
                            });
                            mininav_canvas.mousewheel(function(ev, delta, deltaX, deltaY) {
                                mouse_event(ev, 'zoom', deltaX, deltaY);
                            });
                        }

                        $this.mediaview('reset');

                    } else {

                        draw();

                    }
                };

                var image = canvas.siblings('img');

                if (image.length == 0) {
                    /* Pre-load thumbnail into viewport for quick view */
                    image = img.clone();
                    image.one('load', function() {
                        load_port(image);
                        var loader = loading.clone().insertBefore(canvas);

                        /* Load the real image */
                        image = $('<img/>').attr('src', canvas.attr('data-image'));
                        image.one('load', function() { loader.remove(); load_port(image); });
                        if (image[0].complete) {
                            image.load();
                        }
                    });
                    if (image[0].complete) {
                        image.load();
                    }
                } else {
                    load_port(image);
                }

            });

        },

        zoom : function(factor) {

            return this.each(function() {

                factor = parseFloat(factor);
                var scroll_delta = 1;
                if (factor < -1 && settings.zoom > MIN_ZOOM) {
                    /* zoom out */
                    scroll_delta = 1 / -factor;
                } else if (factor > 1 && settings.zoom < MAX_ZOOM) {
                    /* zoom in */
                    scroll_delta = factor;
                }

                settings.zoom = settings.zoom * scroll_delta;

                /* Zoom to center */
                var im_x = (view_width / 2) - settings.pan[0];
                var im_y = (view_height / 2) - settings.pan[1];
                var new_x = im_x * scroll_delta;
                var new_y = im_y * scroll_delta;

                settings.pan[0] -= (new_x - im_x);
                settings.pan[1] -= (new_y - im_y);

                draw();

            });

        },

        rotate : function(degrees) {

            return this.each(function() {

                settings.rotate += degrees;

                draw();

            });

        },

        reset : function() {

            return this.each(function() {

                settings.last_mouse = [0, 0];
                settings.rotate = 0;

                /* Initial zoom level based on image and viewport dimensions */
                var x = view_width / canvas_image[0].width;
                var y = view_height / canvas_image[0].height;
                if (x < y) {
                    settings.zoom = x;
                } else {
                    settings.zoom = y;
                }

                /* Center image */
                var x = (view_width / 2) - ((canvas_image[0].width * settings.zoom) / 2);
                var y = (view_height / 2) - ((canvas_image[0].height * settings.zoom) / 2);
                settings.pan = [x, y];

                draw();

            });

        },

        detect_dimensions : function(options) {

            return this.each(function() {

                var $ul = $(this).children('#container').children('ul');
                var $con = $('#thumb-selector-container');
                var $sel = $('#thumb-selector');
                var $sidebar = $('#sidebar');
                var $canvas = $('canvas:visible');
                var $doc = $(document);

                view_height = $doc.height();
                view_width = $doc.width();
                if (!($doc.fullScreen())) {
                    view_width -= $sidebar.outerWidth();
                }
                $ul.css('height', view_height + 'px');
                $ul.css('width', view_width + 'px');

                if ($canvas.length > 0) {
                    $canvas[0].width = view_width;
                    $canvas[0].height = view_height;
                    if (ctx) { draw(); }
                }

                /* Enable scrollbar on thumbnails if needed. */
                var con_height = $con.height();
                var thumbs_height = $sel.height();

                if (con_height >= thumbs_height) {
                    $con.removeClass('overflowing');
                    return;
                }

                $con.addClass('overflowing');

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
