function sendData(){

    $("#go_button").click(function(event){

        var ticker = $("#ticker").val().trim();

        $("#loading").show();
        $("#content").hide();

        $.ajax({
            url: '/results',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'ticker':ticker}),
            success: function(response){

                $("#loading").hide();
                evi = response.evi;
                eviKeys = Object.keys(evi);
                eviValues = Object.values(evi)
                $("#query_results").empty();

                for (let i=0; i<eviKeys.length; i++){

                    var newDiv = $(document.createElement("div"));
                    newDiv.attr("id", "q"+String(i+1));
                    newDiv.attr("class", "container-fluid m-3");
                    
                    newDiv.append("<h4> Q"+String(i+1)+". "+eviKeys[i]+"</h4>");
                    // $("#table_of_content").append("<div>"+String(i+1)+". "+eviKeys[i]+"</div>")
                    $.each(eviValues[i], function(ind, val){
                        var eviText = String(ind+1)+". "+val;
                        if (ind<2){
                            newDiv.append("<div id=q"+String(i+1)+"_a"+String(ind+1)+">"+eviText+"<div/>");
                        } else{
                            newDiv.append("<div id=q"+String(i+1)+"_a"+String(ind+1)+" style='display:none'>"+eviText+"<div/>");
                        }
                        
                    });

                    newDiv.append("<input class='btn btn-outline-secondary btn-sm' type='button' value='Read More...' id=a"+String(i+1)+"_more>")
                    newDiv.append("<input class='btn btn-outline-secondary btn-sm' type='button' style='display:none' value='Go Back...' id=a"+String(i+1)+"_back>")

                    $("#query_results").append(newDiv);

                };
                $("#content").show();

                for (let i=0; i<eviKeys.length; i++){
                    $("#a"+String(i+1)+"_more").click(function(){

                        for (let j=2; j<eviValues[i].length; j++){
                            $("#q"+String(i+1)+"_a"+String(j+1)).show();
                        };

                        for (let j=0; j<eviKeys.length; j++){
                            if(j != i){
                                $("#q"+String(j+1)).hide();
                            }
                        }

                        $("#a"+String(i+1)+"_more").hide()
                        $("#a"+String(i+1)+"_back").show()

                    })
                }

                for (let i=0; i<eviKeys.length; i++){
                    $("#a"+String(i+1)+"_back").click(function(){

                        for (let j=2; j<eviValues[i].length; j++){
                            $("#q"+String(i+1)+"_a"+String(j+1)).hide();
                        };

                        for (let j=0; j<eviKeys.length; j++){
                            if(j != i){
                                $("#q"+String(j+1)).show();
                            }
                        }

                        $("#a"+String(i+1)+"_more").show()
                        $("#a"+String(i+1)+"_back").hide()

                    })
                }
                
            },
            error: function(error){
                console.log(error)
            }
        });

        event.preventDefault();

    });


}