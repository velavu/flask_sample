$(function(){
	$('#btnSubmit').click(function(){
        var regionName = $('#regionName').val();
		$.ajax({
			url: '/dataload',
			data: $('form').serialize(),
			type: 'POST',
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
