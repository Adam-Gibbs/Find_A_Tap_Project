// If this goes as planned when I can retrieve data from the database and then
// load it onto the javascript, it will go into teh function and i will be each
// row of tap where then it will be presented on the webpage
function addTapRow(data){
  console.log(data);
  for (var i in data) {
    console.log(i);
    var tr = document.createElement("tr"); // tr is table row
    tr.appendChild(document.createTextNode(i));
    document.getElementById('existing-taps').appendChild(tr);
  }
}
