let mymap;
let pathLayer;
let garage = [52.61801563818295, 39.5260868751346];

function LoadMap() {    
    mymap = L.map('mapid').setView([52.647909, 39.660884], 13);
    mymap.on('click', function(e) {
        onMapClick(e);
    });
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png'
	).addTo(mymap);
    DrawAll();
}

function onMapClick(e) {
    console.log(e);
}

function UpdatePath() {
    divPath = document.getElementById("path");
    if (divPath.style.backgroundColor == 'red') {
        pathLayer.addTo(mymap);
        divPath.style.backgroundColor = 'greenyellow';
    } else {
        pathLayer.removeFrom(mymap);
        divPath.style.backgroundColor = 'red';
    }   
}

function DrawAll() {
    pathLayer = L.layerGroup();
    nodesLayer = L.layerGroup();
    for (let i = 0; i < nodes.length; i++) {
        L.circle(L.latLng(nodes[i][0], nodes[i][1]), {
            color: '#00dffc',
            fillColor: '#00dffc',
            fillOpacity: 1,
            radius: 10
        }).addTo(nodesLayer);
    }
    nodesLayer.addTo(pathLayer);
    edgesLayer = L.layerGroup();
    for (let i = 0; i < edges.length; i++) {
        dots = [];
        for (let j = 0; j < edges[i].length; j++) {
            dots.push(L.latLng(edges[i][j][0], edges[i][j][1]));
        }
        L.polyline(dots, { color: '#ffe06e'}).addTo(edgesLayer);
    }
    edgesLayer.addTo(pathLayer);
    L.circle(L.latLng(garage[0], garage[1]), {
        color: '#7a7373',
        fillColor: '#7a7373',
        fillOpacity: 1,
        radius: 100
    }).addTo(mymap);
    pathLayer.addTo(mymap);
}