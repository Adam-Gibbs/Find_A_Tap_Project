// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
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
  AddMarker(position.coords.latitude, position.coords.longitude, "Current Position")
}

// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
function getLocation2() {
  var x = document.getElementById('ERROR');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function sendPosition(position){
  longitude = position.coords.longitude;
  latitude = position.coords.latitude;
  sendData(longitude, latitude);
}

function sendData(long, lat){
  var coordinates = lat+","+ long;
  // var picture = document.forms["pictureForm"]["file"].value;
  // console.log(picture);
  var params = "coordinates="+coordinates;
  console.log(params);
  var IPPacket = new XMLHttpRequest();
  IPPacket.open("POST", '/home/taps/new', true); // true is asynchronous
  IPPacket.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  IPPacket.send(params);
  console.log(params)
  return false;
}
