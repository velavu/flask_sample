$(function(){
	$('#btnSubmit').click(function(){

        function validate(region, layer, rec){
            if (region == "" || layer == "" || rec == "")
            {
                alert("Enter valid inputs!!");
            }
        }
        var regionName = $('#regionName').val();
        var layer = $('#layer').val();
        var records = $('#records').val();
        $("#progress-bar").css( "visibility", "visible");
        validate(regionName, layer, records);
        alert(regionName);
        alert($('input[id=regionName]').val());
        alert(layer);
        alert($('input[id=layer]').val());
        alert(records);
        alert($('input[id=records]').val());
		var formData = {
                'regionName': regionName,
                'layer': layer,
                'records': records
            };
        console.log(formData);
		console.log($('form').serialize());
		$.ajax({
			url: '/dataload',
			data: formData,
			type: 'GET',
			success: function(response){
				console.log(response);
				  $("#div-result").css( "visibility", "visible");
				  $("#progress-bar").css( "visibility", "hidden");

                var json_resp = $.parseJSON(response);
				$("#load_status").html(json_resp.message.load_status);
				$("#region").html(regionName);
				$("#loaded_on").html(json_resp.message.loaded_on);
                $("#div-db-result").css( "visibility", "visible" );
                var dbResult = json_resp.message.result;
                var tblStr = "<table class=\"table\" width=\"100%\">";
                tblStr += "<thead>";
                tblStr += "<tr>";
                tblStr += "<th>"+dbResult[1][0]+"</th>";
                tblStr += "<th>"+dbResult[1][1]+"</th>";
                tblStr += "<th>"+dbResult[1][2]+"</th>";
                tblStr += "<th>"+dbResult[1][3]+"</th>";
                tblStr += "<th>"+dbResult[1][4]+"</th>";
                tblStr += "<th>"+dbResult[1][5]+"</th>";
                tblStr += "</tr>";
                tblStr += "</thead>";
                tblStr += "<tbody>";
                for (var i=2; i <= dbResult.length; i++){
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
				$("#progress-bar").css( "visibility", "hidden");
                $("#div-result-failure").css( "visibility", "visible");
                var json_resp = $.parseJSON(err);
				$("#error-result").html(json_resp.message.error);
				console.log(error);
			}
		});
	});
});
