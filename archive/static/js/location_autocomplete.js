$(document).ready(
	function(){
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
