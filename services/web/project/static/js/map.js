// use AJAX to get the cities as JSON object
document.addEventListener("DOMContentLoaded", ()=>{
    const request = new XMLHttpRequest();
    request.open("GET", "/getCities")
    request.onload = () =>{
        const response = request.responseText
        console.log("AJAX response: ", response)
        L.geoJSON(JSON.parse(response), {
            onEachFeature: onEachCityFeature
        }).addTo(mymap)
    }
    request.send();
})

const mymap = L.map('map').setView([47.7979, 13.0458], 10);


L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

function onEachCityFeature(feature, layer){
    layer.bindPopup(feature.properties.name +
    "-- latitude:" + feature.coordinates[0].toString() + ", longitude:" + feature.coordinates[1].toString() )
    console.log(feature)
}

