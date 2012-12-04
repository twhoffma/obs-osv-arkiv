$(document).ready(
	function(){
		$("#searchbox").autocomplete({
			source: complete_search,
			minLength: 2,
			select: function(event, ui){
				window.location.href = ui.item.value;
				return(false);
			}
		});
	}
);

function complete_search(request, response){
	$.ajax({
		type: "POST",
		url: "/search_autocomplete/",
		data: {
			'query': request.term,
		},
		success: function(data) {
				response($.parseJSON(data));
			}
	});
}
