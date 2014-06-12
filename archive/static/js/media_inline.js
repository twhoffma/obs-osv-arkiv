(function($) {
$(document).ready(function($) {
	$('.media-inline-table').sortable(
				{stop:on_drop, 
				 cancel: "tr:not(.media-row)",
				 delay: 150,
				 axis: "y"
				});
	
	$('.media-inline-table').on('click', 'input', function(ev){
		ev.target.focus();
		//ev.target.click();
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
	
	//$('.media-inline-table').on('change', "select", function(){
	$('.media-inline-table').on('change', 'input[id$="-media"]', function(){
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

	$(".select_media").dialog({
		autoOpen: false 
	});
	
	$('.media-inline-table').on('click', '.select_media_button', function(event){
		$(".select_media").find('input#target').val($(this).parent().find('input[id$="-media"]').attr('id'));
		
		var w = 0.6*$(window).width();
		var h = 0.5*$(window).height();		

		$(".select_media").dialog("option", "width", w);
		$(".select_media").dialog("option", "height", h);
		$(".select_media").dialog("open");
		
		addr = "/filter_media"
		
		$("div.suggested_media").load(addr);
	});

	$("#search_media").on('change', function(){
		$("div.suggest_media").empty();
		$("div.suggest_media").append('<img src="/images/loading.gif" />');
		
		addr = "/filter_media"
		if($("#search_media").val() != ""){
			addr = addr + '?query=' + $("#search_media").val();
		}
		
		$("div.suggested_media").load(addr);
	});

	$("div.suggested_media").on('click', 'a', function(event){
		var target = $(this).parent().parent().parent().parent().find("input#target").val();
		$("#"+target).val($(this).attr('href'));
		$("#"+target).trigger('change');
		event.preventDefault();
		$(".select_media").dialog("close");
	});
});
	
})(jQuery);
	
	/*
	function find_media(){
		$(".select_media").show();
		addr = "/filter_media"
		if($("#search_media").val() != ""){
			addr = addr + '?query=' + $("#search_media").val();
		}
		
		$("div.suggested_media").load(addr);
	}
	*/
