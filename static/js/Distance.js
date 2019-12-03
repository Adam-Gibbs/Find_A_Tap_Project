// https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
// Author Chuck
function getDistanceFromLatLonInKm(lat1, lng1, posID) {
  stuff_obj = readUrl()
  var lat2 = stuff_obj['lat']
  var lng2 = stuff_obj['lng']
  console.log("LAT = " + lat2 + "LNG = " + lng2)
  var p = 0.017453292519943295;    // Math.PI / 180
  var c = Math.cos;
  var a = 0.5 - c((lat2 - lat1) * p)/2 +
          c(lat1 * p) * c(lat2 * p) *
          (1 - c((lng2 - lng1) * p))/2;

  var d = 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
  d = d.toFixed(2);
  document.getElementById(posID).innerHTML = d + " km"
}

// https://makitweb.com/read-and-get-parameters-from-url-with-javascript/
function readUrl(url){
 
  var para_str = '';
 
  // Checking url is defined or not
  if(url == undefined){
   /* url variable is not defined */
   // get url parameters
   url = window.location.href; // e.g. !num1=43&num2=23
   var split_url = url.split('!');
   para_str = split_url[1];
   if(para_str != undefined){
    var parts = para_str.split('&');
  
  }else{
   /* url variable is defined */
   var split_url = url.split('!');
   para_str = split_url[1];
   if(para_str != undefined){
    var parts = para_str.split('&');
   } 
  }
  
  // Check arguments are defined or not
  if( para_str != undefined && para_str != '' ){
   var parameter_obj = {}; // Object
  
   // looping through all arguments and store in Object
   for(var i=0;i<parts.length;i++){
    var split_val = parts[i].split('=');
  
    // Check argument is available or not e.g. !num1=43&
    if(split_val[0] == undefined || split_val[0] == '' )
      continue;
    var value = split_val[1];
    // Check value is available or not e.g. !num1=43&num2= or !num1=43&num2
    if(value == undefined){
      value = ""; // Assign space if value is not defined
    }
 
    parameter_obj[split_val[0]] = value; 
    
   }
  
    // Print all arguments
    return parameter_obj;
      
  }else{
      return 'No arugment found';
  }
  
 }
}