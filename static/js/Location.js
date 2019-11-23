// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
function getLocation() {
  console.log("hello")
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
  var address = getAddress();
  latText.innerHTML = position.coords.latitude;
  lngText.innerHTML = position.coords.longitude;
  sendData(address, lngText, latText);
  AddMarker(position, "Current Position")
}

function sendData(long, lat){
  var coordinates = lat+","+ long;
  var params = "coordinates="+coordinates;
  console.log(params);
  var IPPacket = new XMLHttpRequest();
  IPPacket.open("POST", '/home/taps/new', true); // true is asynchronous
  IPPacket.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  IPPacket.send(params);
  console.log(params)
  return false;
}
