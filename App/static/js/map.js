const mymap = L.map('map').setView([47.7979, 13.0458], 10);


L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

console.log(cities)
// const cities = [{"type":"Point","coordinates":[13.0205,47.8407]}, {"type":"Point","coordinates":[35.444,12.45454]}, {"type":"Point","coordinates":[13.0974,47.6839]}, {"type":"Point","coordinates":[13.0458,47.7979]}]

// const marker = L.marker([51.5, -0.09]).addTo(mymap);
L.geoJSON(cities).addTo(mymap)