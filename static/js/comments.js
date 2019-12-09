function Addcomment() {

    //Add JQUery AJAX to send tapID
    var comment = document.forms["commentForm"]["inputComment"].value;
    var params = 'inputComment='+comment;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/AddComment', true); // true is asynchronous
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
        console.log(xhttp.responseText);
        document.getElementById("txt").innerHTML = xhttp.responseText;
    } else {
        console.error(xhttp.statusText);
    }
    };
    xhttp.send(params);
    return false;
}
