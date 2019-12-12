// Function to get current user location
// Date: 18/12/2019
// Author:
// Link: https://www.w3schools.com/html/html5_geolocation.asp
function getLocation() {
  var x = document.getElementById('ERROR');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setLink);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function setLink(position) {
  var link = document.getElementById("NewTapLink");
  link.setAttribute("href", `/home/taps/near/page=$0$/!lat=${position.coords.latitude}&lng=${position.coords.longitude}`);
  var myMap = document.getElementById("mapid");
  if(myMap){
    if(myMap.classList.contains('giveCurrentLoc')){
      AddMarker(position.coords.latitude, position.coords.longitude, 'Current Location');
    }

    if(myMap.classList.contains('DraggableMarker')){
      AddDragMarker(position.coords.latitude, position.coords.longitude)
    }

    if(myMap.classList.contains('TapWaypoint')){
      AddMarker(document.getElementById('lat').innerHTML, document.getElementById('lng').innerHTML, document.getElementById('pop').innerHTML)
    }

    if(myMap.classList.contains('giveTaps')){
      $.ajax({
        type : "POST",
        url : "/givetaps",
        data: JSON.stringify({'lat':position.coords.latitude, 'lng': position.coords.longitude}),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            result.forEach(item => AddTapMarker(item['Lat'], item['Lng'], item['Address'], item['Image'], item['ID']));
            GoTo(position)
        }
    });
    }
  }
}
