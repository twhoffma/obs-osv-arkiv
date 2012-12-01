(function($) {
$(document).ready(function($) {
	$('.media-inline-table').sortable({stop:on_drop, cancel: "tr:not(.media-row)"});
	    	$('.media-inline-table input').bind('click.sortable mousedown.sortable', function(ev){
		ev.target.focus();
	});

	function on_drop(event, ui) {
		ui.item.parent().find("tr").each(function(){
			$(this).children("td.field-order").find("input").val($(this).index() + 1);
			$(this).removeClass("row1 row2");
			if(($(this).index()+1) % 2 == 0){
				$(this).addClass("row1");
			}else{
				$(this).addClass("row2");
			}
		});
    	}
	
	$('.media-inline-table').on('change', "select", function(){
		if($(this).parent().find('div.media_details').length == 0){
			$(this).parent().append('<div class="media_details"></div>');
		}
	
		$(this).parent().find("div.media_details").load("/media_details?media_pk="+$(this).val());
	});
	
	$('.media-inline-table').on('click', "a[rel='popshowit']",function(event){
		$("div.lightbox").html('<img src="'+$(this).attr("href") + '" style="max-width: 50%; max-height: 50%; z-index: 3200; position: fixed; left: 25%; top: 25%" />');
		$("div.lightbox").show();
		event.preventDefault();
	});
	
	$("div.lightbox").on('click', function(event){
		$("div.lightbox").html('');
		$("div.lightbox").hide();
	});
});
})(jQuery);
