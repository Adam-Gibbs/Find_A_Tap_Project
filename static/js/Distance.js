function getDistanceFromLatLonInKm() {
  var lat1 = document.getElementById('lat').innerHTML;
  var lon1 = document.getElementById('lon').innerHTML;
  var lon2 = document.forms['findDistance']['longitude'].value;
  var lat2 = document.forms['findDistance']['latitude'].value;
  var p = 0.017453292519943295;    // Math.PI / 180
  var c = Math.cos;
  var a = 0.5 - c((lat2 - lat1) * p)/2 +
          c(lat1 * p) * c(lat2 * p) *
          (1 - c((lon2 - lon1) * p))/2;

  var d = 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
  var data = document.getElementById('ans');
  data.innerHTML = d + " km";
}

document.getElementById('submit').onclick = getDistanceFromLatLonInKm;
