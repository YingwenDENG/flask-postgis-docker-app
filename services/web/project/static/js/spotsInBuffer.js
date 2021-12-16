import {addBufferCircle, addFeatureToMap, removeLayers} from "./map.js";

document.addEventListener('DOMContentLoaded', () => {
    let previous_distance;
    //things to do when the page has been loaded
    document.querySelectorAll('button').forEach(
        button => {
            button.onclick = () => {
                const buttonID = (button.id).match(/\d+/)
                const distance = getInputDistance(buttonID)
                console.log(distance)
                if (distance){
                    if( distance !== previous_distance){
                        document.getElementById(`collapse-${buttonID}`).className += " show";
                        const request = new XMLHttpRequest();
                        // to the endpoint `${button.id}` with method "GET"
                        request.open('GET', `/_withinBuffer/${buttonID}/${distance}`);
                        // what to do after receiving response
                        request.onload = () => {
                            const response = request.responseText;
                            console.log(response)
                            const parsedResponse =parseResponseInStr(response)
                            showSpotsResult(buttonID, parsedResponse[0])
                            removeLayers();
                            if(response!=="No spots found."){
                                addFeatureToMap(parsedResponse[1])
                                addBufferCircle(JSON.parse(parsedResponse[2]), distance)
                            }
                        }
                        // actually send the request
                        request.send()
                    }
                    previous_distance = distance;
                } else{
                    removeLayers();
                    showSpotsResult(buttonID, "Please enter search distance.")
                }
            }
        }
    )
});



function getInputDistance(id){
    const val = document.getElementById(`inputDistance-${id}`).value
    return parseInt(val)
}
function showSpotsResult(id, result) {
    document.getElementById(`collapse-${id}`).innerHTML = "<div class='card card-body'>" + result + "</div>"
}

function parseResponseInStr(str){
    return str.split("**")
}