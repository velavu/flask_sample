$(function(){
	$('#btnSubmit').click(function(){
        // Bit of hack
        var layer_attr_count = {
            "cable": 6,
            "boundary": 3,
            "equipment": 5
        };
        var layer_attr_list = {
            "cable": ["id", "technology", "hierarchy", "specification", "start_equipment_id", "end_equipment_id"],
            "boundary": ["id", "owner", "type"],
            "equipment": ["id", "technology", "hierarchy", "specification", "structure_id"]
        };
        function validate(region, layer, rec){
            if (region == "" || layer == "" || rec == "")
            {
                alert("Enter valid inputs!!");
            }
        }
        function move_progress_bar(w=0){
            console.log(w);
            $("#progress-bar-val").css( "width", w+"%");
            setTimeout(function(){
                w += 5;
                if(w <= 100){
                    move_progress_bar(w);
                }
            }, 2000);
            //this is funny, i expect this to be finished before 40 secs :P
        }
        var regionName = $('#regionName').val();
        var layer = $('#layer').val();
        var records = $('#records').val();
        $("#progress-bar").css( "visibility", "visible");
        console.log("Before");
        move_progress_bar(0);
        console.log("After");
        $("#div-result").css( "visibility", "hidden");
        $("#div-db-result").css( "visibility", "hidden");
        validate(regionName, layer, records);
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
                for (var x=0; x < layer_attr_count[layer]; x++)
                {
                    tblStr += "<th>"+layer_attr_list[layer][x]+"</th>";
                }
                tblStr += "</tr>";
                tblStr += "</thead>";
                tblStr += "<tbody>";
                for (var i=1; i < dbResult.length; i++){
                    tblStr += "<tr>";

                    for (var x=0; x < layer_attr_count[layer]; x++)
                    {
                        tblStr += "<td>"+dbResult[i][x]+"</td>";
                    }
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
