var geojson;
var mymap;
var colors; 

$(document).ready(function() {
mymap = L.map('mapid').setView([40.76, -73.97], 12);

L.tileLayer('https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoieHV0aGVyIiwiYSI6ImNpenEzY3o3azAwemQyd255bG5oYjdjeTMifQ.WsMX8VNOdpiU1d-DgCgLXA', {
		attribution: 'mapbox',
		maxZoom: 18
		}).addTo(mymap);

	getcolors().then(function(resp) {
		colors = resp;
		getGEOJson().then(function (resp) {

		geojson = JSON.parse(resp)
		L.geoJSON(geojson, 
			{
				"opacity": 0.9,
				onEachFeature: labelEachFeature,
				style: function (feature) 
				{
					if (feature.properties.cluster === -1)  {
						return {color: "#" + colors.undefined};
					} else {
						return {color: "#" + colors.colors[feature.properties.cluster]};
					}
				}
			}).addTo(mymap);
		});
	});
});

function labelEachFeature(feature, layer) {
	if (feature.properties) {
		layer.bindPopup(feature.properties.COUNTYFP10 +"-"+ feature.properties.TRACTCE10 + " Cluster: " + feature.properties.cluster);
	}
	//var label = L.marker(layer.getBounds().getCenter(), {
	//	icon: L.divIcon({
	//		className: 'label',
	//		html: feature.properties.COUNTYFP10 +"-"+ feature.properties.TRACTCE10,
	//		iconSize: [100,40]
	//	})
	//}).addTo(mymap);
}

function long2tile(lon,zoom) {return (Math.floor((lon+180)/360*Math.pow(2,zoom))); }
function lat2tile(lat,zoom) { return (Math.floor((1-Math.log(Math.tan(lat*Math.PI/180) + 1/Math.cos(lat*Math.PI/180))/Math.PI)/2 *Math.pow(2,zoom))); }

function getGEOJson() {
	return $.get('jsonout.geojson')
}

function getcolors() {
	return $.get('colors.json')
}
