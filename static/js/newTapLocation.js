// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
function getLocation() {
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
  sendData(longitude, latitude);
}

function sendData(long, lat){
  var params = "latitude="+lat+"&longitude="+long;
  console.log(params);
  var IPPacket = new XMLHttpRequest();
  IPPacket.open("POST", '/home/taps/new', true); // true is asynchronous
  IPPacket.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  IPPacket.send(params);
  console.log(params)
  return false;
}
