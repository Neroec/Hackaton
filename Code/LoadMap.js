let mymap;
let data;

function LoadMap() {    
    mymap = L.map('mapid').setView([52.647909, 39.660884], 13);
    mymap.on('click', function(e) {
        onMapClick(e);
    });    
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png'
	).addTo(mymap);
    for (let i = 0; i < nodes.length; i++) {
        L.circle(L.latLng(nodes[i][0], nodes[i][1]), {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 1,
            radius: 10
        }).addTo(mymap);
    }
    for (let i = 0; i < edges.length; i++) {
        dots = [];
        for (let j = 0; j < edges[i].length; j++) {
            dots.push(L.latLng(edges[i][j][0], edges[i][j][1]));
        }
        L.polyline(dots, { color: 'green'}).addTo(mymap);
    }
}

function onMapClick(e) {

}