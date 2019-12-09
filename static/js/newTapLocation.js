// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
function getCoordinates() {
  var x = document.getElementById('ERROR');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendPosition);
  } else {
    x.innerHTML = "Getting location is not supported by this browser.";
  }
}

function sendPosition(position){
  longitude = position.coords.longitude;
  latitude = position.coords.latitude;
  document.getElementById("longitude").value = longitude;
  document.getElementById("latitude").value = latitude;
  document.getElementById('form').submit();
}
