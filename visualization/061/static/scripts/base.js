var geojson;
var mymap;
var colors; 
var curLayer;
var levels;

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
		curLayer = L.geoJSON(geojson, 
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
			})
		curLayer.addTo(mymap);
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
	$.get('/levels').then(function(resp) {
		levels = JSON.parse(resp);
	});
	return $.get('jsonout.geojson')
}

function up() {
	var current = parseFloat($('#test').val());
	for (var i = 0; i < levels.length; i++) {
		if (levels[i][0] > current) {
			$('#test').val(levels[i][0]);
			return getNewValue();
		}
	}
}

function down() {
	var current = parseFloat($('#test').val());
	for (var i = 0; i < levels.length; i++) {
		if (levels[i][0] >= current) {
			$('#test').val(levels[i-1][0]);
			return getNewValue();
		}
	}
}

function getcolors() {
	return $.get('colors.json')
}

function getLevel(level) {
	return $.get('/json/'+ level)
}

function getNewValue() {
   replace($('#test').val())
   $.get('/count/' + $('#test').val()).then(function(resp) {
		$('#clusterCount').html(resp + " clusters at this level");
   });
}

function replace(level) {
	getLevel(level).then(function(resp) {

		mymap.removeLayer(curLayer);
		geojson = JSON.parse(resp)
		curLayer = L.geoJSON(geojson,
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
			})
		curLayer.addTo(mymap);

	});
}
