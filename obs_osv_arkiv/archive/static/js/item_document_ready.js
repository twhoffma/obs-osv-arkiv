$("#navigation_autocomplete").keyup(
	function(event){
	if (event.keyCode == 13){
		var value = $("#navigation_autocomplete").val();
		window.location.replace('/admin/archive/item/?item_number__icontains='+value);	
}
	}
);

$("#id_keywords").autocomplete({
	source: complete_tag,
	minLength: 0,
	select: add_suggestion
});
	
$("#id_materials").autocomplete({
	source: complete_tag,
	minLength: 0,
	select: add_suggestion
});

/* IN USE */
$('#id_feature_media').bind('change', function(){
	var selection = $('option:selected', this).text();
	var e = $('#id_img_feature_media')
	e.attr('src', '/media/'+selection);
});		
	
/* IN USE */	
$('#id-area').bind("change", function(){
	var area = $(this).val();
	$('#id_room').children("option").remove();
	
	$.ajax({
		type: "POST",
		url: "/room_autocomplete/",
		data: {
			'area': area,
		},
		success: function(data) {
			/*alert(data);*/
			var rooms = $.parseJSON(data);
			$('#id-room').children('option').remove();
			$.each(rooms,
				function(){
					/*alert(this);*/
					$('#id-room').append($('<option></option>').val(this).html(''+this));
				}
			);
		}
	});
});
