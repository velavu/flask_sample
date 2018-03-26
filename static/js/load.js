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
                $("#div-db-result").css( "visibility", "visible" );
                var dbResult = json_resp.message.result;
                var tblStr = "<table class=\"table\" width=\"100%\">";
                for (var i=0; i < 1; i++){
                    tblStr += "<thead>";
                    tblStr += "<tr>";
                    tblStr += "<th>"+dbResult[i][0]+"</th>";
                    tblStr += "<th>"+dbResult[i][1]+"</th>";
                    tblStr += "<th>"+dbResult[i][2]+"</th>";
                    tblStr += "<th>"+dbResult[i][3]+"</th>";
                    tblStr += "<th>"+dbResult[i][4]+"</th>";
                    tblStr += "<th>"+dbResult[i][5]+"</th>";
                    tblStr += "</tr>";
                    tblStr += "</thead>";
                }
                tblStr += "<tbody>";
                for (var i=1; i < dbResult.length; i++){
                    tblStr += "<tr>";
                    tblStr += "<td>"+dbResult[i][0]+"</td>";
                    tblStr += "<td>"+dbResult[i][1]+"</td>";
                    tblStr += "<td>"+dbResult[i][2]+"</td>";
                    tblStr += "<td>"+dbResult[i][3]+"</td>";
                    tblStr += "<td>"+dbResult[i][4]+"</td>";
                    tblStr += "<td>"+dbResult[i][5]+"</td>";
                    tblStr += "</tr>";
                }
                tblStr += "</tbody>";
                tblStr += "</table>";
                summary = "<span> Completed </span>";
                resultData = tblStr + summary;
				$("#div-db-result").html(tblStr);
			},
			error: function(err){
                $("#div-result-failure").css( "visibility", "visible");
                var json_resp = $.parseJSON(err);
				$("#error-result").html(json_resp.message.error);
				console.log(error);
			}
		});
	});
});
