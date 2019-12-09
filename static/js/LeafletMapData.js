var mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(mymap);

function AddTapMarker(latitude, longitude, address, imgaddress, tapID) {
    var popup = '<p class="lead">' + address + '</p> <img style="width: 100%; border-radius: 5%;" src="' + imgaddress + '"alt="Tap Image"> <a href="/home/taps/' + tapID + '/info" class="btn btn-info" style="margin: 10px; color: white;">More Info</a> <a href="/home/taps/' + tapID + '/location" class="btn btn-primary" style="margin: 10px; color: white;">Go To &rarr;</a>';
    console.log(popup)
    L.marker([latitude, longitude]).addTo(mymap)
        .bindPopup(popup).openPopup();
}

function AddMarker(latitude, longitude, popup) {
    L.marker([latitude, longitude]).addTo(mymap)
    .bindPopup(popup).openPopup();
}

function AddDragMarker(latitude, longitude) {
    var dragMark = L.marker([latitude, longitude],{
        draggable: true
    }).addTo(mymap)
    .bindPopup('Drag me to the tap location').openPopup();

    dragMark.on("drag", function(e) {
        var marker = e.target;
        var position = marker.getLatLng();
        console.log(new L.LatLng(position.lat, position.lng));
        document.getElementById("longitude").value = position.lng;
        document.getElementById("latitude").value = position.lat;
    });
}

function GoTo(position) {
    mymap.setView(new L.LatLng(position.coords.latitude, position.coords.longitude), 15);
}

function RouteFromMe(latitudeTo, longitudeTo) {
    var x = document.getElementById('ERROR');
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(Route);
    } else {
      x.innerHTML = "Geolocation is not supported by this browser.";
    }

    function Route(position) {
        longitudeFrom = position.coords.longitude;
        latitudeFrom = position.coords.latitude;
        L.Routing.control({
            lineOptions: {
                styles: [{color: 'lightblue', weight: 4}],
            },
            router: L.Routing.mapbox('pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                profile : 'mapbox/walking'
            }),
            waypoints: [
                L.latLng(latitudeFrom, longitudeFrom),
                L.latLng(latitudeTo, longitudeTo)
            ]
            }).addTo(mymap);
    }
  }
