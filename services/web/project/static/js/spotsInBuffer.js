import {addBufferCircle, addFeatureToMap, removeLayers} from "./map.js";

$(document).ready(function () {
    $("button").each(function () {
        let previous_distance=0;
        $(this).on("click", function (){
            removeLayers();
            const target_id = $(this).attr("id").split("-")[1]
            const inputID="inputDistance-" + target_id.toString()
            const distance = parseFloat($("#" + inputID).val())
            console.log(target_id, inputID, distance)
            if (distance){
                if(distance!== previous_distance){
                    // if a result distance is given
                    $.ajax({
                        type: "POST",
                        url: '/_searchInBuffer',
                        data: {
                            t_id: target_id,
                            search_distance: distance
                        }
                    }).done(function (response){
                        if (response !==""){
                            console.log(response)
                            showSpotsResult(target_id, response.collection)
                            addFeatureToMap(response.cities)
                            addBufferCircle(response.target_coordinate, distance)
                        } else {
                            showSpotsResult(target_id, "No spots found.")
                        }
                    })
                }
            } else {
                showSpotsResult(target_id, "Please enter a search distance.")
            }
            previous_distance=distance
        })
        }
    )

})

function showSpotsResult(id, result) {
    let innerHTML=""
    result.forEach((e)=>{
        innerHTML += "<span class=\"badge bg-warning m-1 \">" + e + "</span>"
    })
    document.getElementById(`collapse-${id}`).innerHTML = innerHTML
    // document.getElementById(`collapse-${id}`).innerHTML = "<div class='card card-body'>" + result + "</div>"
}
