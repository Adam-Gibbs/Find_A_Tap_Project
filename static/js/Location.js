// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
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
  link.setAttribute("href", `/home/taps/near/page=0/lat=${position.coords.latitude}/lng=${position.coords.longitude}`);
  showPosition(position);
}

function showPosition(position) {
  AddMarker(position.coords.latitude, position.coords.longitude, "Current Position");
}

// function getLocation taken from w3school - https://www.w3schools.com/html/html5_geolocation.asp
function getLocation2() {
  var x = document.getElementById('ERROR');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendPosition);
  } else {
    x.innerHTML = "Getting locatrion is not supported by this browser.";
  }
}

function sendPosition(position){
  longitude = position.coords.longitude;
  latitude = position.coords.latitude;
  sendData(longitude, latitude);
}

function sendData(long, lat){
  // var fd = new FormData;
  var picture = document.forms["pictureForm"]["image"].value;
  // fd.append("picture", picture)
  console.log(picture);
  var params = "latitude="+lat+"&longitude="+long+"&picture="+picture;
  console.log(params);
  var IPPacket = new XMLHttpRequest();
  IPPacket.open("POST", '/home/taps/new', true); // true is asynchronous
  IPPacket.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  IPPacket.send(params);
  console.log(params)
  return false;
}
