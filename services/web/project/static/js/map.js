// // use AJAX to get the cities as JSON object
// document.addEventListener("DOMContentLoaded", ()=>{
//     const request = new XMLHttpRequest();
//     request.open("GET", "/getCities")
//     request.onload = () =>{
//         const response = request.responseText
//         console.log("AJAX response: ", response)
//         // L.geoJSON(JSON.parse(response), {
//         //     onEachFeature: onEachCityFeature
//         // }).addTo(mymap)
//         addFeatureToMap(response)
//     }
//     request.send();
// })


export function addAllFeaturesToMap(){
    // use AJAX to get the cities as JSON object
    document.addEventListener("DOMContentLoaded", ()=>{
        const request = new XMLHttpRequest();
        request.open("GET", "/_getCities")
        request.onload = () =>{
            const response = request.responseText
            console.log("AJAX response: ", response)
            addFeatureToMap(response)
        }
        request.send();
    })
}

const mapTiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
});

const mymap = L.map('map').setView([47.7979, 13.0458], 13).addLayer(mapTiles);



function onEachCityFeature(feature, layer){
    layer.bindPopup(feature.properties.name +
    " -- longitude:" + feature.coordinates[0].toString() + ", latitude:" + feature.coordinates[1].toString() )
    console.log(feature)
}

export function addFeatureToMap(features){
    // JSON.parse: parses a JSON string, constructing the JS value or object
    L.geoJSON(JSON.parse(features), {
        onEachFeature: onEachCityFeature
    }).addTo(mymap)
}

export function removeLayers(){
    mymap.eachLayer(function(layer) {
        if (!!layer.toGeoJSON) {
            mymap.removeLayer(layer);
        }
    });
}

export function addBufferCircle(centroid, distance){
    L.circle(centroid, {
        color: "yellow",
        fillColor: "#eec671",
        fillOpacity: 0.5,
        radius: distance
    }).addTo(mymap)
}