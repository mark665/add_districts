var map;
var group;
var clusterer;
var statesLayer;

function numKeys(obj){
    var count = 0;
    for(var prop in obj)
    {
		count++;
	}
	return count;
}

$(document).ready(function() {
	
	map = new L.Map('map');
    group = new L.LayerGroup();
    
    var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/e74bf6d54e334b95af49cbb6b91a6d18/998/256/{z}/{x}/{y}.png',
    cloudmadeAttrib = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
    cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttrib});
    
    var latlng = new L.LatLng(37.2442, -89.6946);
    map.setView(latlng, 5).addLayer(cloudmade);
    
	clusterer = new LeafClusterer(map, [], {gridSize: 50, maxZoom: 15});
	clusterer.clearMarkers();
	
	state_ids = new Array();
	statesLayer = new L.GeoJSON(null);
    
    //Load states polygons
    addStates();
    
    var overlayMaps = {
        "States": statesLayer
    };
    
    var layersControl = new L.Control.Layers(null, overlayMaps);
    map.addControl(layersControl);

	

	addResultMarkers();

	
});


function addStates(){
    var url = "/index.json?layer=States";
    $.getJSON(url, function(data) {
        $.each(data.features, function(i, feature) {
            statesLayer.addGeoJSON(feature);
            state_ids.push(feature.id);
        });
        
        console.log(state_ids.length + " states poly loaded.");
    });
    
    // attach a popup window to each crime
    statesLayer.on("featureparse", function (e){
        e.layer.bindPopup(e.properties.name);
    });
}

function addResultMarkers() {
	var json;
	$.ajax({
		'cache': false,
		'async': true,
		'global': false,
		'url': '/index.json?layer=results',
		'dataType': "json",
		'success': function (data) {
			json = data;
			//layerIcon = new myIcon('http://www2.lichfielddc.gov.uk/myarea/images/icons/'+ layer +'.png');
			var geojson = new L.GeoJSON(null, {
				//pointToLayer: function(latlng) { return new L.Marker(latlng, {icon: layerIcon}); }
				pointToLayer: function(latlng) { return new L.Marker(latlng); }
			});
			var mapBounds = new L.LatLngBounds();
			num = 0;
			geojson.on('featureparse', function(e) {
				type = e.geometryType;
				
				var popupText = e.properties.popupContent;
				e.layer.bindPopup(popupText);

				
				if (e.geometryType == "Point") {
					mapBounds.extend(e.layer._latlng);
				} else {
					for (nextLayer in e.layer._layers) break;
					for (n in e.layer._layers[nextLayer]._latlngs) {
						mapBounds.extend(e.layer._layers[nextLayer]._latlngs[n]);
						e.layer._layers[nextLayer].setStyle({opacity: 1, weight: 2});
					}
				}
				num++;
			});
			
			
			geojson.addGeoJSON(json);
			if (type == "Point") {
				var markers=[];
				for (x in geojson._layers) {
					markers.push(geojson._layers[x]);
				}
				clusterer.addMarkers(markers);
			} else {
				group.addLayer(geojson);
				map.addLayer(group);
			}
			
			map.fitBounds(mapBounds);
			
			
			$('.item').click(function() {
				currentlayer = this.id;
				if (geojson._layers[currentlayer]._layers == undefined) {
					try {
						geojson._layers[currentlayer].openPopup();
					} catch(e) {
						map.setView(geojson._layers[currentlayer]._latlng, 16);
						geojson._layers[currentlayer].openPopup();
					}
				} else {
					for (nextLayer in geojson._layers[currentlayer]._layers) break;
					latlng = geojson._layers[currentlayer]._layers[nextLayer]._latlngs[0];
					geojson._layers[currentlayer]._layers[nextLayer]._openPopup({latlng: latlng})
				}
				return false;
			});
		}
	});
}



