$(document).ready(
	function(){
		$("#navigation_autocomplete").keyup(
			function(event){
				if (event.keyCode == 13){
					var value = $("#navigation_autocomplete").val();
					//alert(''+value);
					window.location.replace('/admin/archive/item/?item_number__icontains='+value);	
				}
			}
		);
		
		$("#id_keywords").autocomplete({
			source: complete_keyword,
			minLength: 0,
			select: add_suggestion
		});
		
		$("#id_materials").autocomplete({
			source: complete_material,
			minLength: 0,
			select: add_suggestion
		});
		
		/*
		$('.field-media').find('select').each(function(){
			$(this).on('change', function(){
				var val = $(this).val();
				alert(''+$(this).val());	
			});
		});

		$('.media_change').on('change', function(){
			alert('value='+$(this).val())
		});
		*/
		
		/* IN USE */
		$('#id_feature_media').bind('change', function(){
			var selection = $('option:selected', this).text();
			var e = $('#id_img_feature_media')
			e.attr('src', '/media/'+selection);
		});		
	
		/* IN USE */	
		$('#id_area').bind("change", function(){
			var area = $(this).val();
			$('#id_room').children("option").remove();
	
			$.ajax({
				type: "POST",
				url: "/room_autocomplete/",
				data: {
					'query': area,
				},
				success: function(data) {
					var rooms = $.parseJSON(data);
					$('#id_room').children('option').remove();
					$('#id_room').append($('<option></option>').val('').html('---------'));
					$.each(rooms,
						function(){
							$('#id_room').append($('<option></option>').val(this[0]).html(''+this[1]));
						}
					);

					$('#id_room').trigger('change');
				}
			});
		});
		
		/* IN USE */	
		$('#id_address').bind("change", function(){
			var addr = $(this).val();
			$('#id_area').children("option").remove();
	
			$.ajax({
				type: "POST",
				url: "/area_autocomplete/",
				data: {
					'query': addr,
				},
				success: function(data) {
					/*alert(data);*/
					var rooms = $.parseJSON(data);
					$('#id_area').children('option').remove();
					$('#id_area').append($('<option></option>').val('').html('---------'));
					$.each(rooms,
						function(){
							/*alert(this);*/
							$('#id_area').append($('<option></option>').val(this[0]).html(''+this[1]));
						}
					);
					
					$('#id_area').trigger('change');
				}
			});
		});
		
		/* IN USE */	
		$('#id_room').bind("change", function(){
			var room = $(this).val();
			$('#id_location').children("option").remove();
	
			$.ajax({
				type: "POST",
				url: "/location_autocomplete/",
				data: {
					'query': room,
				},
				success: function(data) {
					var rooms = $.parseJSON(data);
					$('#id_location').children('option').remove();
					$('#id_location').append($('<option></option>').val('').html('---------'));
					$.each(rooms,
						function(){
							$('#id_location').append($('<option></option>').val(this[0]).html(''+this[1]));
						}
					);

					$('#id_location').trigger('change');
				}
			});
		});
	}
);

function add_suggestion(event, ui){
	terms = $(this).val().split(",");
	terms.pop();
	terms.push(ui.item.label);
	$(this).val(terms.join(","));
	return(false);
}

function add_topic_select(event, ui){
	$('#topic_subtopic_helper').val(ui.item.label);
	//alert($('#topic_subtopic_helper').val());
	return(true);
}

function complete_topic(request, response){
	$.ajax({
		type: "POST",
		url: "/topic_autocomplete/",
		data: {
			'topic': request.term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}

function prepare_subtopic_search(event, ui){
	var term = this.value;
	var subtopic_id = $(this).attr('id');
	var topic_id = subtopic_id.replace('-subtopic', '-topic');
	$('#topic_subtopic_helper').val($('#'+topic_id).val());	
}

function complete_subtopic(request, response){
	var topic = $('#topic_subtopic_helper').val();
	
	$.ajax({
		type: "POST",
		url: "/subtopic_autocomplete/",
		data: {
			'topic': topic,
			'subtopic': request.term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}

function complete_tag(request, response){
	terms = request.term.split(",");
	if(terms.length == 1){
		term = terms[0];
	}else{
		term = terms.slice(-1)[0];
	}
	
	$.ajax({
		type: "POST",
		url: "/tag_autocomplete/",
		data: {
			'query': term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}

function complete_material(request, response){
	terms = request.term.split(",");
	if(terms.length == 1){
		term = terms[0];
	}else{
		term = terms.slice(-1)[0];
	}
	
	$.ajax({
		type: "POST",
		url: "/material_autocomplete/",
		data: {
			'query': term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}

function complete_keyword(request, response){
	terms = request.term.split(",");
	if(terms.length == 1){
		term = terms[0];
	}else{
		term = terms.slice(-1)[0];
	}
	
	$.ajax({
		type: "POST",
		url: "/keyword_autocomplete/",
		data: {
			'query': term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}

function delete_topic(){
	var total = $("#id_form-TOTAL_FORMS").val();
	total--;
	
	p = $(this).parent('div');
	//test = p.attr('class');	
	//alert("Parent id: "+test);
	p.remove();	
	$("#id_form-TOTAL_FORMS").val(total);
	
		
	//alert('total forms after removal: '+$("#id_form-TOTAL_FORMS").val());
}

function add_topic(){
	var total = $("#id_form-TOTAL_FORMS").val();
	
	last_topic = $("#id-topic_formset>div:last").prev();
	
	new_topic_id = total;	

	last_topic.clone(true).removeClass('div-form-'+(total-1)).addClass('div-form-'+total).appendTo('#id-topic_formset');
	new_topic = $('.div-form-'+total);
	
	new_topic.children().each(
		function(){
			var child_id = $(this).attr('id');
			var child_name = $(this).attr('name');
			
			if(child_id){	
				child_id = child_id.replace('-'+(total-1)+'-','-'+total+'-');	
				child_name = child_name.replace('-'+(total-1)+'-','-'+total+'-');	
				$(this).attr('id', child_id);
				$(this).attr('name', child_name);
				$(this).val('');
			}
		}
	);
	

	total++;
	$("#id_form-TOTAL_FORMS").val(total);
}

function add_location(){
	$('#dialog-add_location').dialog({
		height: 200,
		modal: true
	});
}
