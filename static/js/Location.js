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
  link.setAttribute("href", `/home/taps/near/page=0/!lat=${position.coords.latitude}&lng=${position.coords.longitude}`);
  var myMap = document.getElementById("mapid");
  if(myMap){
    showPosition(position);

    if(myMap.classList.contains('giveTaps')){
      $.ajax({
        type : "POST",
        url : "/givetaps",
        data: JSON.stringify({'lat':position.coords.latitude, 'lng': position.coords.longitude}),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            result.forEach(item => AddMarker(item[2], item[3], item[1]));
            GoTo(position)
        }
    });
    }
  }
}

function showPosition(position) {
  AddMarker(position.coords.latitude, position.coords.longitude, "Current Position");
}
