function getLocation() {
  var x = document.getElementById('ERROR');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  var lngText = document.getElementById('lon');
  var latText = document.getElementById('lat');
  latText.innerHTML = position.coords.latitude;
  lngText.innerHTML = position.coords.longitude;
}
