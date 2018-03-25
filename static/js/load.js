$(function(){
	$('#btnSubmit').click(function(){
        var regionName = $('#regionName').val();
		var formData = {
                'regionName': $('input[id=regionName]').val()
            };
		console.log($('form').serialize());
		$.ajax({
			url: '/dataload',
			data: formData,
			type: 'GET',
			success: function(response){
				console.log(response);
				  $("#div-result").css( "visibility", "visible" );

                var json_resp = $.parseJSON(response);
				$("#load_status").html(json_resp.message.load_status);
				$("#region").html(regionName);
				$("#loaded_on").html(json_resp.message.loaded_on);
			},
			error: function(error){
                $("#div-result-failure").css( "visibility", "visible" );
				console.log(error);
			}
		});
	});
});
