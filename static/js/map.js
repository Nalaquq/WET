
var location=fetch("http://ip-api.com/json/")
        response = json.loads(client_location.text)
        longitude = response["lon"]
        latitude = response["lat"]
    except:
        longitude = -161.902701
        latitude = 59.757774
        pass

var map = L.map('map').setView([{{latitude}}, {{longitude}}], 13);
		
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    		maxZoom: 19,
	    		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo(map);

var drawnItems = new L.FeatureGroup();
     		
		map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
	              edit: { 
			      featureGroup: drawnItems
			               }
	          });
     		
		map.addControl(drawControl);
		map.on('draw:created', function (e) {
			    var type = e.layerType;
			    var layer = e.layer; 
			
		
			//push layer edits to Flask 
			    var shape=layer.toGeoJSON()
			    var shape_for_db=JSON.stringify(shape);
			    $.ajax({
			    url: '/map', 
			    type: 'POST',
			    data: shape_for_db,
			    })
			    .done(function(result){
			    console.log(result)
			})
			//add layer to map 
			drawnItems.addLayer(layer);
	
		}); 
