var mymap = L.map('mapid').setView([48.843, 17.298], 7);
	//L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	L.tileLayer('https://maps.wikimedia.org/osm-intl/${z}/${x}/${y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var geojsonMarkerOptions = {
	radius: 8,
	fillColor: "#ff5000",
	color: "#ffffff",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.75
};

function pointToLayer(feature, latlng) {
	geojsonMarkerOptions.fillColor = feature.properties["marker-color"]
	return L.circleMarker(latlng, geojsonMarkerOptions);
}

function onEachFeature(feature, layer) {
	layer.bindPopup(feature.properties.title + "</br>" + 
		feature.properties.description + "</br>" +
		feature.properties.type);
}

function geojsonLoaded() {
	featuresObject = JSON.parse(geojson.response)
	L.geoJSON(featuresObject, {
		pointToLayer: pointToLayer,
		onEachFeature: onEachFeature
	}).addTo(mymap)
} 

var geojson = new XMLHttpRequest();
geojson.open("GET", "https://raw.githubusercontent.com/jonnyrobbie/gpx2json/master/jonnyrobbie.geojson");
geojson.addEventListener("load", geojsonLoaded);
geojson.send()
