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
	}
);

function add_suggestion(event, ui){
	terms = $(this).val().split(",");
	terms.pop();
	terms.push(ui.item.label);
	$(this).val(terms.join(","));
	return(false);
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
